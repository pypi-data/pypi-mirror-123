# This file is part of CFELPyUtils.
#
# CFELPyUtils is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# CFELPyUtils is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with CFELPyUtils.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014-2021 Deutsches Elektronen-Synchrotron DESY,
# a research centre of the Helmholtz Association.
"""
This module contains several implementations of algorithms that detect Bragg peaks in detector frame
data.
It provides access to the individual implementations via their respective class,
and a convenience function to return an instantiated object.
"""

from typing import Dict, Any
from cfelpyutils.peakfinding.peakfinder8 import Peakfinder8PeakDetection


def get_peakfinder(
    peakfinder_type: str, peakfinder_config: Dict[str, Any]
) -> Peakfinder8PeakDetection:
    """ This is a convenience function to request the appropriate Peakfinder object.

    :argument peakfinder_type: The name of the peakfinder to be requested:

        * peakfinder8
        * [placeholder]

    :argument peakfinder_config: A dictionary holding the configuration parameters of
        the requested peakfinder.

    :raises ValueError: If peakfinder_type is wrong.

    """
    if peakfinder_type == "peakfinder8":
        return Peakfinder8PeakDetection(
            max_num_peaks=peakfinder_config["max_num_peaks"],
            asic_nx=peakfinder_config["asic_nx"],
            asic_ny=peakfinder_config["asic_ny"],
            nasics_x=peakfinder_config["nasics_x"],
            nasics_y=peakfinder_config["nasics_y"],
            adc_threshold=peakfinder_config["adc_threshold"],
            minimum_snr=peakfinder_config["minimum_snr"],
            min_pixel_count=peakfinder_config["min_pixel_count"],
            max_pixel_count=peakfinder_config["max_pixel_count"],
            local_bg_radius=peakfinder_config["local_bg_radius"],
            min_res=peakfinder_config["min_res"],
            max_res=peakfinder_config["max_res"],
            bad_pixel_map_filename=peakfinder_config["bad_pixel_map_filename"],
            bad_pixel_map_hdf5_path=peakfinder_config["bad_pixel_map_hdf5_path"],
            radius_pixel_map=peakfinder_config["radius_pixel_map"],
        )
    else:
        raise ValueError(f"Unknown peakfinder type: {peakfinder_type}")
