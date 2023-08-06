"""Library version variables.

The package version stored in python variables.
Following a semantic versioning, the package version is stored as tuple
and for convenience concatenated to a string variable.
"""

version_tuple = (0, 2, 2, "")
"""The (semantic) version of the module implemented as tuple with major, minor, bugfix and alpha/beta/dev version."""

version = "{}.{}.{}{}".format(*version_tuple)
"""The (semantic) version of the module concatenated to a string."""

