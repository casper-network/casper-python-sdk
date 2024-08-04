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

    async def get_response_1(
        self,
        endpoint: Endpoint,
        request_id: RequestID,
    ) -> Response:
        """Dispatches request to a remote node binary port & returns response.

        :param request: Request to be dispatched.
        :returns: Remote node binary server response.

        """
        request: Request = _get_request(
            endpoint,
            request_id,
            self.connection_info.binary_request_version,
            self.connection_info.chain_protocol_version
        )

        request_bytes: bytes = codec.encode(request, True)

        response_bytes: bytes = await _get_response_bytes(
            self.connection_info.host,
            self.connection_info.port,
            request_bytes
        )


    async def get_response(self, request: Request) -> Response:
        """Dispatches request to a remote node binary port & returns response.

        :param request: Request to be dispatched.
        :returns: Remote node binary server response.

        """
        request_bytes: bytes = codec.encode(request, True)
        response_bytes: bytes = await _get_response_bytes(self.connection_info, request_bytes)

        return _parse_response_bytes(request_bytes, response_bytes)


def _get_request(
    endpoint: Endpoint,
    request_id: RequestID,
    binary_request_version: int,
    chain_protocol_version: str,
) -> Request:
    """Returns a remote binary server request header.

    """
    return Request(
        endpoint=endpoint,
        header=RequestHeader(
            binary_request_version,
            ProtocolVersion.from_semvar(chain_protocol_version),
            request_id,
        )
    )


async def _get_response_bytes(server_host: str, server_port: int, request_bytes: bytes) -> bytes:
    """Dispatches a remote binary server request and returns the request/response pair.

    """
    # Set stream reader & writer.
    reader, writer = await asyncio.open_connection(server_host, server_port)

    # Write request.
    writer.write(request_bytes)
    writer.write_eof()

    # Read response.
    response_bytes: bytes = (await reader.read(-1))

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return response_bytes


def _parse_response_bytes(request_bytes: bytes, response_bytes: bytes) -> Response:
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
    bstream, length = codec.decode_u32(response_bytes)
    assert \
        len(bstream) == length, \
        "Response decoding error: inner byte length mismatch"

    # TODO: clarify why need to offset by 2
    bstream = bstream[2:]

    # Assert request echo.
    assert \
        bstream.find(request_bytes) == 0, \
        "Response decoding error: request bytes not found"

    # Assert response decoding.
    bstream, response = codec.decode(bstream[len(request_bytes):], Response)
    assert \
        len(bstream) == 0, \
        "Response decoding error: unconsumed bytes"

    return response
