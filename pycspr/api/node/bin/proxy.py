import asyncio
import random
import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    RequestHeader, \
    RequestID, \
    Response
from pycspr.api.node.bin.types.domain import \
    ProtocolVersion


class Proxy:
    """Node BINARY server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.connection_info = connection_info

    async def invoke_endpoint(
        self,
        endpoint: Endpoint,
        request_id: RequestID,
    ) -> Response:
        """Dispatches request to a remote node binary port & returns response.

        :param endpoint: Endpoint to be invoked.
        :param request_id: Identifier of request to be dispatched.
        :returns: Remote node binary server response.

        """
        # Set request.
        request: Request = Request(
            header=RequestHeader(
                self.connection_info.binary_request_version,
                ProtocolVersion.from_semvar(self.connection_info.chain_protocol_version),
                endpoint,
                request_id,
            )
        )

        # Set request bytes.
        bytes_request: bytes = codec.encode(request, prepend_length=True)

        # Set response bytes - i.e. call server.
        bytes_response: bytes = await _get_response_bytes(self.connection_info, bytes_request)

        # Set response.
        bytes_rem, response = codec.decode(bytes_response, Response)
        assert len(bytes_rem) == 0, "Uncomsumed response bytes"

        return response


async def _get_response_bytes(connection_info: ConnectionInfo, bytes_request: bytes) -> bytes:
    """Dispatches a remote binary server request and returns the request/response pair.

    """
    # Set stream reader & writer.
    reader, writer = await asyncio.open_connection(connection_info.host, connection_info.port)

    # Write request.
    writer.write(bytes_request)
    writer.write_eof()

    # Read response.
    bytes_response: bytes = (await reader.read(-1))

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return _parse_response(bytes_request, bytes_response)


def _parse_response(bytes_request: bytes, bytes_response: bytes) -> bytes:
    """Parses a node's binary port response.

    """
    assert \
        isinstance(bytes_response, bytes) is True, \
        "Response decoding error: response is not bytes"

    bytes_rem, length = U32.from_bytes(bytes_response)
    assert \
        len(bytes_rem) == length, \
        "Response decoding error: inner byte length mismatch"

    # TODO: clarify why need to offset by 2
    assert \
        bytes_rem[2:].find(bytes_request) == 0, \
        "Response decoding error: request bytes not found"

    return bytes_response
