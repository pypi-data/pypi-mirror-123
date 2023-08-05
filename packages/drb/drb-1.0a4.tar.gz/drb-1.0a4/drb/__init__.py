from ._version import get_versions
from .item import DrbItem
from .node import DrbNode

__version__ = get_versions()['version']
del get_versions
__all__ = ['DrbItem', 'DrbNode']
