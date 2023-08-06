from pkg_resources import get_distribution as _get_distribution
__version__ = _get_distribution("k1lib").version

from ._hidden.hiddenFile import hiddenF
from ._basics import *
from . import format
from . import website
from . import nn
from .data import *
from . import selector
from .callbacks import Callback, Callbacks
from . import callbacks
from ._learner import Learner
from .schedule import Schedule, ParamScheduler
from . import viz

#from . import gE
from . import eqn

from . import mo as _mo; from functools import partial as _partial
class _Mo: # element properties
    def __init__(self):
        self.__dict__.update({k: _mo.__dict__[k] for k in _mo.__all__})
for _name, _f in _mo._a.items():
    setattr(_Mo, _name, property(_partial((lambda self, _f: _f()), _f=_f)))
mo = _Mo()


from .bioinfo import *
from . import imports