# miscset


"""Main module and public API.

Public API
----------

Direct Imports
``````````````

Contains imports to all submodules relevant for public usage,
so that a direct import is not necessary. This allows:

.. code-block:: python

    import miscset
    miscset.sh.run("echo hello")
    # >>> CompletedProcess(args='bash -s', returncode=0, stdout='hello\\n', stderr='')

Logging
-------

Defines a default :py:mod:`logging` handler as a
:py:class:`logging.NullHandler` to allow usage of loggers
in methods of this package.
The handler can be redefined by a custom python module
importing methods from `miscset` and to custom logs:

.. code-block:: python

    import logging
    import miscset

    handler = logging.StreamHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # this command prints now any debug messages using the log handler specified above
    miscset.sh.run("echo hello")
    # >>> shell stdin is echo hello
    # >>> shell runner is ['bash -s']
    # >>> shell stdout is
    # >>> hello
    # >>> shell stderr is
    # >>> shell return code is 0
    # >>> CompletedProcess(args='bash -s', returncode=0, stdout='hello\\n', stderr='')
"""


import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


from . import dt
from . import io
from . import sh
from . import files
from . import tables
from ._version import version
