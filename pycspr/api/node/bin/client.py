import typing

from pycspr.api.node.bin.connection import ConnectionInfo
from pycspr.api.node.bin.proxy import Proxy


class Client():
    """Node BINARY server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's BINARY port.

        """
        self.proxy = Proxy(connection_info)

    def get_block_header(self, decode=True):
        self.proxy.get_block_header()
        pass
