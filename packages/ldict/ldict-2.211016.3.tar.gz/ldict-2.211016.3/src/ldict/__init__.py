from .appearance import decolorize
from .config import setup
from .empty import Empty
from .functionspace import FunctionSpace
from .ldict_ import Ldict

ldict = Ldict

empty = Empty()
"""The empty object is used to induce a ldict from a dict"""

Ø = empty
"""UTF-8 alias for the empty object, it is used to induce a ldict from a dict. AltGr+Shift+o in most keyboards."""

decolorize = decolorize
