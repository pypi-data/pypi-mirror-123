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

from cfelpyutils.geometry import load_crystfel_geometry


@pytest.fixture
def detector_geometry(tmp_path):
    """ Example geometry of an EigerX2 16M in 4M mode """

    geometry = """photon_energy = 20000
adu_per_eV = 0.0001
clen = 0
coffset = -0.0
res = 5814.0

0/dim2 = fs
0/dim1 = ss
0/dim0 = %
0/data = /entry/data/data

0/min_fs = 0
0/max_fs = 2067
0/min_ss = 0
0/max_ss = 2161
0/corner_x = -1034
0/corner_y = -1081
0/fs = 1.0x +0.0y
0/ss = 0.0x +1.0y
"""
    geometry_file = tmp_path / "example.geom"
    geometry_file.write_text(geometry)
    return load_crystfel_geometry(str(geometry_file))[0]


small_detector_geometry_data = """photon_energy = 20000
adu_per_eV = 0.0001
clen = 0
coffset = -0.0
res = 1.0

0/dim2 = fs
0/dim1 = ss
0/dim0 = %
0/data = /entry/data/data

0/min_fs = 0
0/max_fs = 4
0/min_ss = 0
0/max_ss = 4
0/corner_x = -2
0/corner_y = -2
0/fs = 1.0x +0.0y
0/ss = 0.0x +1.0y
"""

@pytest.fixture
def small_detector_geometry(tmp_path):
    """ Geometry of an imaginary detector with 5x5 pixels"""
    geometry_file = tmp_path / "example.geom"
    geometry_file.write_text(small_detector_geometry_data)
    return load_crystfel_geometry(str(geometry_file))[0]