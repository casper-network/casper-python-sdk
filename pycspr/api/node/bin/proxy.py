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

    async def get_response(
        self,
        endpoint: Endpoint,
        request_id: RequestID,
    ) -> Response:
        """Dispatches request to a remote node binary port & returns response.

        :param request: Request to be dispatched.
        :returns: Remote node binary server response.

        """
        request_bytes: bytes = _get_request_bytes(
            endpoint,
            request_id,
            self.connection_info
        )
        response_bytes: bytes = await _get_response_bytes(
            self.connection_info,
            request_bytes
        )
        print(response_bytes.hex())

        return _get_response(request_bytes, response_bytes)


def _get_request_bytes(
    endpoint: Endpoint,
    request_id: RequestID,
    connection_info: ConnectionInfo,
) -> bytes:
    """Returns a binary server request.

    """
    request: Request = Request(
        endpoint=endpoint,
        header=RequestHeader(
            connection_info.binary_request_version,
            ProtocolVersion.from_semvar(connection_info.chain_protocol_version),
            request_id,
        )
    )

    return codec.encode(request, True)


def _get_response(request_bytes: bytes, response_bytes: bytes) -> Response:
    """Parses a node's binary port response.

    :param request: Original request.
    :param request_bytes: Original request as raw bytes.
    :param response_bytes: Server response as raw bytes.
    :returns: Parsed, i.e. decoded, response.

    """
    # Assert response data type.
    assert \
        isinstance(response_bytes, bytes) is True, \
        "Response decoding error: response is not bytes"

    # Assert length of inner byte stream.
    bytes_rem, length = codec.decode_u32(response_bytes)
    assert \
        len(bytes_rem) == length, \
        "Response decoding error: inner byte length mismatch"

    # TODO: clarify why need to offset by 2
    bytes_rem = bytes_rem[2:]

    # Assert request echo.
    assert \
        bytes_rem.find(request_bytes) == 0, \
        "Response decoding error: request bytes not found"

    # Assert response decoding.
    bytes_rem, response = codec.decode(response_bytes, Response)
    assert \
        len(bytes_rem) == 0, \
        "Response decoding error: unconsumed bytes"

    return response


async def _get_response_bytes(connection_info: ConnectionInfo, request_bytes: bytes) -> bytes:
    """Dispatches a remote binary server request and returns the request/response pair.

    """
    # Set stream reader & writer.
    reader, writer = await asyncio.open_connection(connection_info.host, connection_info.port)

    # Write request.
    writer.write(request_bytes)
    writer.write_eof()

    # Read response.
    response_bytes: bytes = (await reader.read(-1))

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return response_bytes
