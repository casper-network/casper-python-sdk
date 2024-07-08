import asyncio

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
    return Request(
        body = request_body,
        header = get_request_header(connection_info, request_type, request_id),
    )


def get_request_header(
    connection_info: ConnectionInfo,
    request_type: RequestType,
    request_id: int = None
) -> RequestHeader:
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
) -> Response:
    # Set TCP stream reader & writer.
    reader, writer = await asyncio.open_connection(connection_info.host, connection_info.port)

    # Set request.
    request: Request = get_request(connection_info, request_type, request_body, request_id)

    # Set request byte stream.
    bstream_out: bytes = codec.encode(request)
    bstream_out = codec.encode_u32(len(bstream_out)) + bstream_out
    print(bstream_out)

    # Dispatch request.
    writer.write(bstream_out)
    writer.write_eof()

    # Set response byte stream.
    bstream_in: bytes = (await reader.read(-1))

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return get_response_decoded(bstream_in, request_id)


def get_response_decoded(bstream: bytes, request_id: int) -> Response:
    print(bstream)

    # Assert byte stream is parseable.
    if isinstance(bstream, bytes) is False:
        raise ValueError("Invalid response: byte stream is empty")
    if len(bstream) <= 4:
        raise ValueError("Invalid response: byte stream too small to decode")

    # Assert inner byte stream length.
    bstream, length = codec.decode_u32(bstream)
    if length != len(bstream):
        raise ValueError("Invalid response: bytes length prefix mismatch")

    # Decode request.
    bstream, length = codec.decode_u32(bstream[2:])
    remaining, request = codec.decode(bstream[:length], Request)
    if len(remaining) != 0:
        raise ValueError("Invalid response: request bytes only partially consumed")
    if request.header.id != request_id:
        raise ValueError("Invalid response: request id mismatch")

    # Decode response.
    bstream, response = codec.decode(bstream[length:], Response)
    if len(bstream) != 0:
        raise ValueError("Invalid byte stream: only partially consumed")

    print(response)

    return response
