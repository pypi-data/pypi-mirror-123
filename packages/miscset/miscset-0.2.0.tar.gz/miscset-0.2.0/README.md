# miscset

[![Build Status](https://travis-ci.com/setempler/miscset.py.svg?branch=main)](https://travis-ci.com/setempler/miscset.py) 
[![codecov.io](https://codecov.io/github/setempler/miscset.py/coverage.svg?branch=main)](https://codecov.io/github/setempler/miscset.py)
[![pypi](https://img.shields.io/pypi/v/miscset.svg)](https://pypi.org/project/miscset/)

## About

🛠 Miscellaneous set of helpful methods for [Python](https://www.python.org).

* Find *data* and *time* formatting wrapper in the module `miscset.dt`.
* Find *stream i/o* methods in the module `miscset.io`.
* Find *filesystem* methods in the module `miscset.files`.
* Find *subprocess* methods in the module `miscset.sh`.
* Find *tabular data conversion* methods in the module `miscset.tables`.

## Usage

`</>` Example using methods from this package:

```python
# import the library
import miscset

# print the current date/time
print(miscset.dt.now())
# >>> 2021-06-06 12:34:56

# return a shell command standard output
print(miscset.sh.run("uname").stdout)
# >>> Darwin

# convert data types to and from tables (pandas.DataFrame)
print(miscset.tables.list_to_df([[1,2,3], ["a","b","c"]]))
# >>>   col1 col2
# >>> 0    1    a
# >>> 1    2    b
# >>> 2    3    c
```

📚 See all method descriptions and a full feature list in the documentation hosted on [miscset.readthedocs.io](https://miscset.readthedocs.io).

## Installation

💾 The installation is as simple as running the command `pip install miscset`,
as the package is hosted on [pypi.org](https://pypi.org/project/miscset).

## Developing

💻 Please find the source code hosted on [github.com](https://github.com/setempler/miscset.py).

For developers, follow this workflow:

* Create a clean python virtual environment via `python3 -m venv .venv.miscset`.
* Load th3 python environment with `source .venv.miscset/bin/actviate`.
* Install developer libraries using `make init`.
* Install the module using `make install`.
* Build the HTML documentation with `make docs`.
* Run tests using `make test`.
* Add issues, pull requests, comments and other contributions to [github](https://github.com/setempler/miscset.py/issues).

## Copying

© See file `LICENSE`.