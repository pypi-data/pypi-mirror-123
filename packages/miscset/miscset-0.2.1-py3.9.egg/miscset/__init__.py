# miscset


"""Main module and public API.

Version
-------

The library version can be identified by the `version` object.

.. exec_code::
    :caption: Example code:
    :caption_output: Result:

    import miscset
    print(miscset.version)

Direct Imports
--------------

The module imports to all submodules relevant for public usage,
so that a direct import is not necessary. This allows:

.. exec_code::
    :caption: Example code:
    :caption_output: Result:

    import miscset
    print(miscset.sh.run)

Logging
-------

Defines a default :py:mod:`logging` handler as a
:py:class:`logging.NullHandler` to allow usage of loggers
in methods of this package.
The handler can be redefined by a custom python module
importing methods from `miscset` and to custom logs:

.. exec_code::
    :caption: Example code:
    :caption_output: Result:

    import logging
    import miscset

    handler = logging.StreamHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # this command prints now any debug messages using the log handler specified above
    out = miscset.sh.run("echo hello")
    print(out)
"""


import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


from . import dt
from . import io
from . import sh
from . import files
from . import tables
from ._version import version

foo = "bar"