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
Functions for getting data from CrystFEL stream output files.
"""

import io
import re
from warnings import warn

import numpy  # type: ignore
import pandas  # type: ignore

_dec = r"[+-]?[\d\.]+(?:e[+-]?\d+)?"
abc_star_re = re.compile(f"([abc]star) = ({_dec}) ({_dec}) ({_dec}) nm\^-1")
det_shift_re = re.compile(f"predict_refine/det_shift x = ({_dec}) y = ({_dec}) mm")
cell_param_re = re.compile(
    f"Cell parameters ({_dec}) ({_dec}) ({_dec}) nm, ({_dec}) ({_dec}) ({_dec}) deg"
)

PEAK_LIST_START_MARKER = "Peaks from peak search"
PEAK_LIST_END_MARKER = "End of peak list"
CHUNK_START_MARKER = "----- Begin chunk -----"
CHUNK_END_MARKER = "----- End chunk -----"
CRYSTAL_START_MARKER = "--- Begin crystal"
CRYSTAL_END_MARKER = "--- End crystal"
REFLECTION_START_MARKER = "Reflections measured after indexing"
REFLECTION_END_MARKER = "End of reflections"


def _read_to_line(f, marker):
    marker += "\n"
    for line in f:
        if line == marker:
            return


def _buffer_to_line(f, marker):
    marker += "\n"
    s = io.StringIO()
    for line in f:
        if line == marker:
            break
        s.write(line)
    s.seek(0)
    return s


def _parse_crystal(f, refl_tbl):
    d = {}

    for line in f:
        line = line.strip()
        if line == CRYSTAL_END_MARKER:
            return d
        elif line == REFLECTION_START_MARKER:
            if refl_tbl:
                d["reflections"] = pandas.read_csv(
                    _buffer_to_line(f, REFLECTION_END_MARKER), delim_whitespace=True,
                )
            else:
                _read_to_line(f, REFLECTION_END_MARKER)
        elif line.startswith("Cell parameters "):
            m = cell_param_re.match(line)
            if m:
                vals = numpy.array([float(v) for v in m.groups()])
                d["Cell parameters/lengths"] = vals[:3]
                d["Cell parameters/angles"] = vals[3:]
            else:
                warn(f"Failed to parse cell parameters line {line!r}")
        elif line.startswith(("astar ", "bstar ", "cstar ")):
            m = abc_star_re.match(line)
            if m:
                key, *vals = m.groups()
                d[key] = numpy.array([float(v) for v in vals])
            else:
                warn(f"Failed to parse [abc]star line {line!r}")
        elif line.startswith("predict_refine/det_shift "):
            m = det_shift_re.match(line)
            if m:
                vals = numpy.array([float(v) for v in m.groups()])
                d["predict_refine/det_shift"] = vals
            else:
                warn(f"Failed to parse [abc]star line {line!r}")
        else:
            # Simple "key = value" line
            pair = line.split("=", 1)
            if len(pair) != 2:
                warn(f"Unrecognised line: {line!r}")
                continue

            d[pair[0].strip()] = pair[1].strip()


def parse_chunk(f, *, peak_tbl=True, refl_tbl=True):
    """Parse one chunk (one image/event) from a file-like object to a dictionary

    This reads from the current position to the 'End chunk' marker or the end
    of the file.
    """
    d = {"crystals": []}

    for line in f:
        line = line.strip()
        if line == CHUNK_END_MARKER:
            return d

        elif line == PEAK_LIST_START_MARKER:
            if peak_tbl:
                d["peaks"] = pandas.read_csv(
                    _buffer_to_line(f, PEAK_LIST_END_MARKER), delim_whitespace=True,
                )
            else:
                _read_to_line(f, PEAK_LIST_END_MARKER)
        elif line == CRYSTAL_START_MARKER:
            d["crystals"].append(_parse_crystal(f, refl_tbl))

        else:
            # Simple "key = value" or "key: value" line
            pair = line.split("=", 1)
            if len(pair) != 2:
                pair = line.split(":", 1)
                if len(pair) != 2:
                    warn(f"Unrecognised line: {line!r}")
                    continue

            d[pair[0].strip()] = pair[1].strip()

    # Either this was a chunk from iter_chunks, without the end_chunk marker,
    # or an incomplete chunk at the end of the file.
    return d


def iter_chunks(stream_file):
    """Yield chunks, each describing one image/event, as StringIO objects

    The StringIO objects can be used with parse_chunk to extract information.
    The Begin chunk & End chunk marker lines are not included in the output.
    """
    if not hasattr(stream_file, "read"):
        with open(stream_file, "r") as f:
            yield from iter_chunks(f)
        return

    for line in stream_file:
        if line.strip() == CHUNK_START_MARKER:
            yield _buffer_to_line(stream_file, CHUNK_END_MARKER)


def parse_chunks(stream_file, *, peak_tbl=True, refl_tbl=True):
    """Iterate over chunks in a stream file, yielding dicts of image info

    If you don't need the tables of peaks found or reflections, skipping these
    (``peak_tbl=False, refl_tbl=False``) may make reading much faster.

    The values of typical "key = value" lines are left as strings in the dicts,
    so it's up to the caller to convert fields it uses into numbers, e.g.
    ``int(d['num_peaks'])``. However, some lines which contain several numbers
    are parsed (Cell parameters, a/b/c star, 2D detector shift) into small
    NumPy arrays.
    """
    if not hasattr(stream_file, "read"):
        with open(stream_file, "r") as f:
            yield from parse_chunks(f, peak_tbl=peak_tbl, refl_tbl=refl_tbl)
        return

    for line in stream_file:
        if line.strip() == CHUNK_START_MARKER:
            yield parse_chunk(stream_file, peak_tbl=peak_tbl, refl_tbl=refl_tbl)
