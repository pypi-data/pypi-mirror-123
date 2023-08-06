"""Library version variables.

The package version stored in python variables.
Following a semantic versioning, the package version is stored as tuple (`version_` variable)
and for convenience concatenated to a string variable (`version_string_`).
"""

version_tuple = (0, 2, 1, "")
"""The (semantic) version of the module implemented as tuple with major, minor, bugfix and alpha/beta version."""

version = "{}.{}.{}{}".format(*version_tuple)
"""The (semantic) version of the module concatenated to a string."""

