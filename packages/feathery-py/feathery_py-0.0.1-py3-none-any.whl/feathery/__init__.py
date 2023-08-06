"""
Feathery
A asynchronous, scaling first Discord API package wrapper. With built-in cli for code generation
and deploying/running your package. Simple database integration and State caching for Discord API
objects.
"""

__name__ = "Feathery"
__version__ = "v0.0.1"
__author__ = "NotOddity"

# local package imports
from . import commands
from . import events
from . import resources
from . import types

# local module imports
from .async_core import *
from .aws_core import *
from .command import *
from .component import *
from .gateway import *
from .multi_core import *
from .payload import *
from .service import *
from .shard import *