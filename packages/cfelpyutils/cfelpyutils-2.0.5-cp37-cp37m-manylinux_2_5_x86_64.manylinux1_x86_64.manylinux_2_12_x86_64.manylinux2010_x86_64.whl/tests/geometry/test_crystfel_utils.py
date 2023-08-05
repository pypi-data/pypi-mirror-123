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
"""
Caveat: This is a very basic test. It has a low coverage and only tests the 'public' function.

TODO: Improve test. Add tests for helper functions.
"""
from collections import OrderedDict

import numpy
import pytest
from cfelpyutils.geometry.crystfel_utils import load_crystfel_geometry
from tests.fixtures import small_detector_geometry_data


def test_load_crystfel_geometry(tmp_path):
    geometry_file = tmp_path / "test.geom"
    geometry_file.write_text(small_detector_geometry_data)

    expected_detector = {
        "bad": OrderedDict(),
        "furthest_in_fs": 0,
        "furthest_in_panel": "0",
        "furthest_in_ss": 5,
        "furthest_out_fs": 5,
        "furthest_out_panel": "0",
        "furthest_out_ss": 5,
        "mask_bad": 0,
        "mask_good": 0,
        "panels": OrderedDict(
            [
                (
                    "0",
                    {
                        "adu_per_eV": 0.0001,
                        "adu_per_photon": pytest.approx(numpy.nan, nan_ok=True),
                        "badrow": "-",
                        "clen": 0.0,
                        "clen_for_centering": pytest.approx(numpy.nan, nan_ok=True),
                        "clen_from": "",
                        "cnx": -2.0,
                        "cny": -2.0,
                        "coffset": -0.0,
                        "data": "/entry/data/data",
                        "dim_structure": ["%", "ss", "fs"],
                        "fsx": 1.0,
                        "fsy": 0.0,
                        "fsz": 0.0,
                        "h": 5,
                        "mask": "",
                        "mask_file": "",
                        "max_adu": numpy.inf,
                        "no_index": False,
                        "orig_max_fs": 4,
                        "orig_max_ss": 4,
                        "orig_min_fs": 0,
                        "orig_min_ss": 0,
                        "rail_x": pytest.approx(numpy.nan, nan_ok=True),
                        "rail_y": pytest.approx(numpy.nan, nan_ok=True),
                        "rail_z": pytest.approx(numpy.nan, nan_ok=True),
                        "res": 1.0,
                        "satmap": "",
                        "satmap_file": "",
                        "ssx": 0.0,
                        "ssy": 1.0,
                        "ssz": 0.0,
                        "w": 5,
                        "xfs": 1.0,
                        "xss": 0.0,
                        "yfs": 0.0,
                        "yss": 1.0,
                    },
                )
            ]
        ),
        "rigid_group_collections": {},
        "rigid_groups": {},
    }
    expected_beam = {
        "photon_energy": 20000.0,
        "photon_energy_from": "",
        "photon_energy_scale": 1.0,
    }
    expected_hdf5_peak_path = ""

    geometry = load_crystfel_geometry(str(geometry_file))

    assert len(geometry) == 3

    assert geometry.detector == expected_detector
    assert geometry.beam == expected_beam
    assert geometry.hdf5_peak_path == expected_hdf5_peak_path
