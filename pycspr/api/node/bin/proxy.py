import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin import types
from pycspr.api.node.bin import utils
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    RequestID


class Proxy:
    """Node BINARY server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.connection_info = connection_info

    async def get_response(self, request: Request) -> bytes:
        # Map request -> bytes
        #
        print(107, request)

        bstream_out: bytes = codec.encode(request, True)

        return bstream_out
