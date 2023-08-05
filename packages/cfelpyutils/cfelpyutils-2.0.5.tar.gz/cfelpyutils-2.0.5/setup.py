# This file is part of CFELPyUtils.
#
# CFELPyUtils is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# CFELPyUtils is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with CFELPyUtils.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014-2021 Deutsches Elektronen-Synchrotron DESY,
# a research centre of the Helmholtz Association.

import numpy
from setuptools import Extension, setup
from Cython.Build import cythonize

peakfinder8_ext = Extension(
    name="cfelpyutils.peakfinding.lib.peakfinder8_extension",
    include_dirs=[numpy.get_include()],
    libraries=["stdc++"],
    sources=[
        "src/peakfinder8_extension/peakfinder8.cpp",
        "src/peakfinder8_extension/peakfinder8_extension.pyx",
    ],
    language="c++",
)


if __name__ == "__main__":
    setup(ext_modules=cythonize(peakfinder8_ext))
