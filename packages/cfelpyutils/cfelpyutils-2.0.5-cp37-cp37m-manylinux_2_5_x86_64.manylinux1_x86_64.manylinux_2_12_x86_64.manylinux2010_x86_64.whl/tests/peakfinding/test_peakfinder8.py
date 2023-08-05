# This file is part of CFELPyUtils.
#
# CFELPyUtils is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# CFELPyUtils is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with CFELPyUtils.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014-2021 Deutsches Elektronen-Synchrotron DESY,
# a research centre of the Helmholtz Association.

import numpy
import pytest
from cfelpyutils.geometry import compute_pix_maps
from cfelpyutils.peakfinding.peakfinder8 import Peakfinder8PeakDetection
from tests.fixtures import detector_geometry


@pytest.fixture
def radius_pixel_map(detector_geometry):
    pixmaps = compute_pix_maps(detector_geometry)
    return pixmaps.r


@pytest.fixture
def peakfinder_config(radius_pixel_map):
    return {
        "max_num_peaks": 2048,
        "asic_nx": 2068,
        "asic_ny": 2162,
        "nasics_x": 1,
        "nasics_y": 1,
        "adc_threshold": 25.0,
        "minimum_snr": 5.0,
        "min_pixel_count": 2,
        "max_pixel_count": 40,
        "local_bg_radius": 3,
        "min_res": 150,
        "max_res": 1250,
        "bad_pixel_map_filename": None,
        "bad_pixel_map_hdf5_path": None,
        "radius_pixel_map": radius_pixel_map,
    }


@pytest.fixture
def detector_image_with_4_peaks():
    image = numpy.random.randint(0, 1000, (2162, 2068), dtype=numpy.uint16)
    image[300:302, 100:102] = [[2000, 50000], [5000, 10000]]
    image[400:402, 100:102] = [[2000, 50000], [5000, 10000]]
    image[500:502, 100:102] = [[2000, 50000], [5000, 10000]]
    image[600:602, 100:102] = [[2000, 50000], [5000, 10000]]
    return image

# TODO: add test with valid bad_pixel_mask
class TestPeakfinder8PeakDetection:
    def test_init(self, peakfinder_config):
        peakfinder = Peakfinder8PeakDetection(**peakfinder_config)
        assert peakfinder._max_num_peaks == peakfinder_config["max_num_peaks"]
        assert peakfinder._asic_nx == peakfinder_config["asic_nx"]
        assert peakfinder._asic_ny == peakfinder_config["asic_ny"]
        assert peakfinder._nasics_x == peakfinder_config["nasics_x"]
        assert peakfinder._nasics_y == peakfinder_config["nasics_y"]
        assert peakfinder._adc_thresh == peakfinder_config["adc_threshold"]
        assert peakfinder._minimum_snr == peakfinder_config["minimum_snr"]
        assert peakfinder._min_pixel_count == peakfinder_config["min_pixel_count"]
        assert peakfinder._max_pixel_count == peakfinder_config["max_pixel_count"]
        assert peakfinder._local_bg_radius == peakfinder_config["local_bg_radius"]
        assert (
            peakfinder._radius_pixel_map == peakfinder_config["radius_pixel_map"]
        ).all()
        assert peakfinder._min_res == peakfinder_config["min_res"]
        assert peakfinder._max_res == peakfinder_config["max_res"]
        assert peakfinder._mask_initialized == False
        assert peakfinder._mask == None

    def test_find_peak(self, peakfinder_config, detector_image_with_4_peaks):
        peakfinder = Peakfinder8PeakDetection(**peakfinder_config)
        peak_list = peakfinder.find_peaks(detector_image_with_4_peaks)
        assert peak_list.num_peaks == 4
        assert len(peak_list.intensity) == 4
        assert len(peak_list.fs) == 4
        assert len(peak_list.ss) == 4
