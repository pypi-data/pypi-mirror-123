# The CFELPyUtils Library

## Introduction

CFELPyUtils is a utility library written in Python and developed at the Center For Free
Electron Laser Science (CFEL) in Hamburg. It contains several functions and classes
that perform various tasks related to the processing of x-ray imaging data. It is used by
several internal and released CFEL software projects.

### Features

- Read and apply geometry information to x-ray detector data
- peak finding algorithm (new in v2.0)
- calibration tool for the AGIPD 1M detector (new in v2.0)
- module for reading [CrystFEL](https://www.desy.de/~twhite/crystfel/) streams (new in v2.0)

Please see the [migration guide](#migration-guide) below before upgrading from CFELPyUtils 0.x or 1.x.

## Installation

The CFELPyUtils library is available on the [Python Package Index](https://pypi.org/)
(PyPI). It can be installed using the 'pip' command:

    pip install cfelpyutils

For Python 2, please use the 1.0 version.

    pip install cfelpyutils==1.0.1

The library can also be installed manually by checking out this repository and running:

    python setup.py install

### Migration Guide

The following table lists functions for which the module affiliation has changes in v2.0.
Please replace all old occurances with the new ones.

| `cfelpyutils-0.x,-1.x` | `cfelpytuils-2` |
| ---------------------- | --------------- |
| `geometry_utils.compute_pix_maps()` | `geometry.compute_pix_maps()` |
| `geometry_utils.compute_visualization_pix_maps()` | `geometry.compute_visualization_pix_maps()` |
| `geometry_utils.apply_geometry_to_data()` | `geometry.apply_geometry_to_data()` |
| `crystfel_utils.load_crystfel_geometry()` | `geometry.load_crystfel_geometry()` |

Please note that `geometry.load_crystfel_geometry()` now returns a namedtuple of `geometry.CrystFELGeometry`.
Previously it returned only a `geometry.TypeDetector`.
This is not the first element of the tuple.

If your code did this before

```python
from cfelpyutils.crystfel_utils import load_crystfel_geometry
geometry = load_crystfel_geometry(path_to_geometry_file)
```

it needs to be changed to something like

```python
from cfelpyutils.geometry import load_crystfel_geometry
geometry_tuple = load_crystfel_geometry(path_to_geometry_file)
geometry = geometry_tuple.detector
```
or
```python
from cfelpyutils.geometry import load_crystfel_geometry
geometry_tuple = cfelpyutils.geometry.load_crystfel_geometry(path_to_geometry_file)
geometry = geometry_tuple[0]
```

## Contributors

The CFELPyUtils library is currently developed in the lab of
[Henry Chapman](https://cid.cfel.de/) at the Center For Free Electron Laser Science
in Hamburg.

Many people from different institutions worlwide contribute code, testing and support
to the project:

* Valerio Mariani
* Anton Barty
* Andrew Morgan
* Thomas A. White
* Thomas Kluyver
* Philipp Middendorf
* Luca Gelisio
* Florian Lauck

If you have any questions or want to contribute, please [contact us](mailto:sc@cfel.de).

## Documentation

Documentation for the CFELPyUtils is available
on [GitLab at DESY](https://cfel-sc-public.pages.desy.de/cfelpyutils/) and
in the [docs/](docs) of the [repository](https://gitlab.desy.de/cfel-sc-public/cfelpyutils).

## Source Code

The source code of the CFELPyUtils library can be found on the DESY GitLab instance:
https://gitlab.desy.de/cfel-sc-public/cfelpyutils
