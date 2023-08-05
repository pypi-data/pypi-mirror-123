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
from cfelpyutils.geometry.geometry import (
    apply_geometry_to_data,
    compute_pix_maps,
    compute_visualization_pix_maps,
)
from tests.fixtures import small_detector_geometry


# TODO: also test with multi panel detector.

def test_compute_pix_maps(small_detector_geometry):
    phi = numpy.array(
        [
            [-2.3561945, -2.0344439, -1.5707964, -1.1071488, -0.7853982],
            [-2.6779451, -2.3561945, -1.5707964, -0.7853982, -0.4636476],
            [3.1415925, 3.1415925, 0.0, 0.0, 0.0],
            [2.6779451, 2.3561945, 1.5707964, 0.7853982, 0.4636476],
            [2.3561945, 2.0344439, 1.5707964, 1.1071488, 0.7853982],
        ],
        dtype=float,
    )
    radius = numpy.array(
        [
            [2.828427, 2.236068, 2.0, 2.236068, 2.828427],
            [2.236068, 1.4142135, 1.0, 1.4142135, 2.236068],
            [2.0, 1.0, 0.0, 1.0, 2.0],
            [2.236068, 1.4142135, 1.0, 1.4142135, 2.236068],
            [2.828427, 2.236068, 2.0, 2.236068, 2.828427],
        ],
        dtype=float,
    )
    x = numpy.array(
        [
            [-2.0, -1.0, 0.0, 1.0, 2.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0],
        ],
        dtype=float,
    )
    y = numpy.array(
        [
            [-2.0, -2.0, -2.0, -2.0, -2.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [2.0, 2.0, 2.0, 2.0, 2.0],
        ],
        dtype=float,
    )
    z = numpy.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    pixel_maps = compute_pix_maps(small_detector_geometry)

    # make arrays 1D and compare lists
    assert list(pixel_maps.phi.ravel()) == pytest.approx(phi.ravel())
    assert list(pixel_maps.r.ravel()) == pytest.approx(radius.ravel())
    # compare 2D arrays
    assert (pixel_maps.x == x).all()
    assert (pixel_maps.y == y).all()
    assert (pixel_maps.z == z).all()


def test_compute_visualization_pix_maps(small_detector_geometry):
    x = numpy.array(
        [
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
        ],
        dtype=int,
    )
    y = numpy.array(
        [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4],
        ],
        dtype=int,
    )

    pixel_maps = compute_visualization_pix_maps(small_detector_geometry)

    assert (pixel_maps.x == x).all()
    assert (pixel_maps.y == y).all()


def test_apply_geometry_to_data(small_detector_geometry):

    data = numpy.array(
        [
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ],
        dtype=int,
    )
    expected_visualization_array = numpy.array(
        [
            [0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    visualization_array = apply_geometry_to_data(data, small_detector_geometry)

    assert (visualization_array == expected_visualization_array).all()
