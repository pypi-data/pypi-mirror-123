# 🛠 miscset

[![Build Status](https://travis-ci.com/setempler/miscset.py.svg?branch=main)](https://travis-ci.com/setempler/miscset.py) 
[![codecov.io](https://codecov.io/github/setempler/miscset.py/coverage.svg?branch=main)](https://codecov.io/github/setempler/miscset.py)
[![pypi](https://img.shields.io/pypi/v/miscset.svg)](https://pypi.org/project/miscset/)

## 📚 About

Miscellaneous set of helpful methods for [Python](https://www.python.org).

* Find simpler *date* and *time* formatting wrapper in the submodule `dt`.
* Find advanced *file system* methods in the module `files`.
* Find collected *stream i/o* methods in the module `io`.
* Find easier *subprocess* methods in the module `sh`.
* Find helpful *tabular data conversion* methods in the module `tables`.

See all method descriptions and a full feature list in the documentation hosted on [miscset.readthedocs.io](https://miscset.readthedocs.io) and many more details and usage examples in the respective submodule documentation.

## 💾 Installation

The installation is as simple as running the command `pip install miscset`,
as the package is hosted on [pypi.org](https://pypi.org/project/miscset).

## 💻 Developing

Please find the source code hosted on [github.com](https://github.com/setempler/miscset.py).

For developers, follow this workflow:

* Create a clean python virtual environment via `python3 -m venv .venv.miscset`.
* Load th3 python environment with `source .venv.miscset/bin/actviate`.
* Install developer libraries using `make init`.
* Install the module using `make install`.
* Build the HTML documentation with `make docs`.
* Run tests using `make test`.
* Add issues, pull requests, comments and other contributions to [github](https://github.com/setempler/miscset.py/issues).

## © Copying

See file `LICENSE`.