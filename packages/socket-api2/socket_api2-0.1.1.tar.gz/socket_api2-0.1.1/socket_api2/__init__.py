__name__ = "socket_api2"
__version__ = "0.1.1"

__author__ = "Da4ndo"
__discord__ = "Da4ndo#0934"
__youtube__ = "https://www.youtube.com/channel/UCdhZa-JISiqwd913nhB8cAw?"
__github__ = "https://github.com/Mesteri05"

from .client import Client, SEND_METHOD
from .server import Server, outstr

SEND_METHOD = SEND_METHOD
Server = Server
Client = Client
outstr = outstr