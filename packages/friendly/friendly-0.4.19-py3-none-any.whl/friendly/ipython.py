from ._ipython import *  # noqa
from friendly_traceback import __version__

# By default, we assume a terminal with a dark background.
set_formatter("dark")  # noqa
print(
    f"friendly_traceback {__version__}; friendly {version}.\nType 'Friendly' for information."
)
