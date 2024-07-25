import asyncio
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
        """Dispatches request to a remote node binary port & returns response.

        :param request: Request to be dispatched.
        :returns: Remote node binary server response.

        """
        # Set request byte stream.
        bstream_request: bytes = codec.encode(request, True)

        return await _get_response(self.connection_info, bstream_request)


async def _get_response(connection_info: ConnectionInfo, bstream_request: bytes) -> bytes:
    """Dispatches a remote binary server request and returns the request/response pair.

    """
    # Set TCP stream reader & writer.
    reader, writer = await asyncio.open_connection(connection_info.host, connection_info.port)

    # Dispatch request.
    writer.write(bstream_request)
    writer.write_eof()

    # Set response byte stream.
    bstream_response: bytes = (await reader.read(-1))

    # Assert request echo.
    assert bstream_request in bstream_response

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return bstream_response
