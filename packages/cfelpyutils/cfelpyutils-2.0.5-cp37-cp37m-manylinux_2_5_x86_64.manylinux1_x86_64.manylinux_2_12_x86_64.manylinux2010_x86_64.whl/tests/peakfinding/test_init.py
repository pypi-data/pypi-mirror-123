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

import pytest
from cfelpyutils.peakfinding import get_peakfinder
from cfelpyutils.peakfinding.peakfinder8 import Peakfinder8PeakDetection


def test_get_peakfinder_with_unknown_peakfinder():
    with pytest.raises(ValueError):
        get_peakfinder("non-existant peakfinder", {})


def test_get_peakfinder_peakfinder8():

    peakfinder_config = {
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
        "radius_pixel_map": None,  # required, but does not cause a problem here.
    }

    peakfinder = get_peakfinder("peakfinder8", peakfinder_config)
    assert isinstance(peakfinder, Peakfinder8PeakDetection)
    assert hasattr(peakfinder, "find_peaks")
