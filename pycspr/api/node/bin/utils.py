import asyncio

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.connection import ConnectionInfo
from pycspr.api.node.bin.types.domain import ProtocolVersion
from pycspr.api.node.bin.types.request.core import Request
from pycspr.api.node.bin.types.request.core import RequestHeader
from pycspr.api.node.bin.types.request.core import RequestType
from pycspr.api.node.bin.types.response.core import Response
from pycspr.api.node.bin.types.response.core import ResponseHeader


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

    # Dispatch request.
    writer.write(codec.encode_u32(len(bstream_out)) + bstream_out)
    writer.write_eof()

    # Set response byte stream.
    bstream_in: bytes = (await reader.read(-1))

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return get_parsed_response(bstream_in)


def get_parsed_response(bstream: bytes) -> Response:
    # Assert byte stream is parseable.
    if isinstance(bstream, bytes) is False:
        raise ValueError("Invalid byte stream: empty")
    if len(bstream) <= 4:
        raise ValueError("Invalid byte stream: too small")

    # Assert inner byte stream length.
    bstream, length = codec.decode_u32(bstream)
    if length != len(bstream):
        raise ValueError("Invalid byte stream: length prefix mismatch")

    # Assert byte stream is consumed after decoding.
    bstream, response = codec.decode_entity(bstream, Response)
    if len(bstream) != 0:
        raise ValueError("Invalid byte stream: only partially consumed")

    return response
