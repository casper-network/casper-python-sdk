import asyncio

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.connection import ConnectionInfo
from pycspr.api.node.bin.types.domain import ProtocolVersion
from pycspr.api.node.bin.types.request.core import Request
from pycspr.api.node.bin.types.request.core import RequestHeader
from pycspr.api.node.bin.types.request.core import RequestType


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
) -> bytes:
    # Set TCP stream reader & writer.
    reader, writer = await asyncio.open_connection(connection_info.host, connection_info.port)

    # Set request.
    request: Request = get_request(connection_info, request_type, request_body, request_id)

    # Set message.
    msg: bytes = codec.encode(request)

    # Dispatch request.
    writer.write(codec.encode_u32(len(msg)) + msg)
    writer.write_eof()

    # Set response.
    response: bytes = (await reader.read(-1))

    # Close stream.
    writer.close()
    await writer.wait_closed()

    return parse_response(response)


def parse_response(response: bytes) -> bytes:
    # Validate that a response was returned.
    if isinstance(response, bytes) is False:
        raise ValueError("Invalid response: expected bytes")

    # Validate length of bytes.
    length = codec.decode_u32(response[0:4])
    if length != len(response[4:]):
        raise ValueError("Invalid response: length prefix mismatch")

    # Destructure response header.
    # TODO
    return response[4:]
