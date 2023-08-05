__title__ = 'Amino.ed'
__author__ = 'Alert Aigul'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Alert'
__version__ = '1.2.21.3'

from .lib import util
from .acm import ACM
from .client import Client
from .sub_client import SubClient
from .socket import Callbacks, SocketHandler
from .lib.util import device, exceptions, headers, helpers, objects, tapjoy
from requests import get
from json import loads

__newest__ = loads(get("https://pypi.python.org/pypi/Amino.ed/json").text)["info"]["version"]

if __version__ != __newest__:
    print(exceptions.LibraryUpdateAvailable(f"New version of {__title__} available: {__newest__} (Using {__version__})"))
