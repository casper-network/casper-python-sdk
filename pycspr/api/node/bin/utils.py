import asyncio
import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Request, \
    RequestHeader, \
    RequestType, \
    Response, \
    ResponseHeader
from pycspr.api.node.bin.types.domain import \
    ProtocolVersion


def get_request(
    connection_info: ConnectionInfo,
    request_type: RequestType,
    request_body: object,
    request_id: int = None
) -> Request:
    """Returns a remote binary server request.

    """
    return Request(
        body = request_body,
        header = get_request_header(connection_info, request_type, request_id),
    )


def get_request_header(
    connection_info: ConnectionInfo,
    request_type: RequestType,
    request_id: int = None
) -> RequestHeader:
    """Returns a remote binary server request header.

    """
    return RequestHeader(
        binary_request_version = connection_info.binary_request_version,
        chain_protocol_version = \
            ProtocolVersion.from_semvar(connection_info.chain_protocol_version),
        type_tag = request_type,
        id = request_id or 0,
    )


async def get_response(
    connection_info: ConnectionInfo,
    request_type: RequestType,
    request_body: object,
    request_id: int = None
) -> bytes:
    """Dispatches a remote binary server request and returns the request/response pair.

    """
    # Set TCP stream reader & writer.
    reader, writer = await asyncio.open_connection(connection_info.host, connection_info.port)

    # Set request.
    request: Request = get_request(connection_info, request_type, request_body, request_id)

    # Set request byte stream.
    bstream_out: bytes = codec.encode(request, True)
    print(bstream_out)

    # Dispatch request.
    writer.write(bstream_out)
    writer.write_eof()

    # Set response byte stream.
    bstream_in: bytes = (await reader.read(-1))
    assert bstream_out in bstream_in

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return bstream_in


def parse_response(bstream: bytes, request_id: int) -> typing.Tuple[Request, Response]:
    # Assert byte stream is parseable.
    if isinstance(bstream, bytes) is False:
        raise ValueError("Invalid response: byte stream is empty")
    if len(bstream) <= 4:
        raise ValueError("Invalid response: byte stream too small to decode")

    # Assert inner byte stream length.
    bstream, length = codec.decode_u32(bstream)
    if length != len(bstream):
        raise ValueError("Invalid response: bytes length prefix mismatch")

    # Assert request decoding and request id match.
    bstream, length = codec.decode_u32(bstream[2:])
    remaining, request = codec.decode(bstream[:length], Request)
    if len(remaining) != 0:
        raise ValueError("Invalid response: request bytes only partially consumed")
    if request.header.id != request_id:
        raise ValueError("Invalid response: request id mismatch")

    # Assert response decoding.
    bstream, response = codec.decode(bstream[length:], Response)
    if len(bstream) != 0:
        raise ValueError("Invalid byte stream: only partially consumed")

    return request, response
