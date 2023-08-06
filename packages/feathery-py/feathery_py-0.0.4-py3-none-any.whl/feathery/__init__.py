"""
Feathery
A asynchronous, scaling first Discord API package wrapper. With built-in cli for code generation
and deploying/running your package. Simple database integration and State caching for Discord API
objects.
"""

__name__ = "feathery-py"
__version__ = "0.0.4"
__author__ = "NotOddity"
__url__ = "https://github.com/NotOddity/feathery"
__description__ = "No description yet"

# local package imports
from . import commands
from . import events
from . import resources
from . import types
from . import exceptions

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