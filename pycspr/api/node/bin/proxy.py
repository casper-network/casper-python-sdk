import asyncio
import typing

from pycspr.api.node.bin import codec
from pycspr.type_defs.chain import ProtocolVersion
from pycspr.type_defs.primitives import U32
from pycspr.api.node.bin.type_defs import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    RequestHeader, \
    RequestID, \
    Response, \
    ResponseAndRequest, \
    RESPONSE_PAYLOAD_TYPE_INFO


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
        request_id: RequestID,
        endpoint: Endpoint,
        payload: typing.Optional[bytes] = None
    ) -> Response:
        """Invokes remote endpoint and returns a response.

        :param request_id: User defined request correlation identifier.
        :param endpoint: Remote endpoint to be invoked.
        :param payload: Optional request payload.
        :returns: Response plus associated payload.

        """
        # Set request.
        request = Request(
            header=RequestHeader(
                self.connection_info.binary_request_version,
                ProtocolVersion.from_semvar(self.connection_info.chain_protocol_version),
                endpoint,
                request_id,
            ),
            payload=payload if payload is not None else bytes([])
        )

        # Set bytes: request.
        bytes_request: bytes = codec.encode(codec.encode(request), bytes)

        # Set bytes: response and request.
        bytes_response_and_request: bytes = \
            await _get_response_bytes(self.connection_info, bytes_request)

        # Set entity: response and request.
        bytes_rem, response_and_request = \
            codec.decode(ResponseAndRequest, bytes_response_and_request)
        assert len(bytes_rem) == 0

        # Set response payload.
        response_and_request.response.payload = _get_response_payload_entity(
            request.header.endpoint,
            response_and_request.response.payload_bytes
        )

        return response_and_request.response


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

    return _parse_response_bytes(bytes_request, bytes_response)


def _get_response_payload_entity(
    endpoint: Endpoint,
    payload_bytes: bytes
) -> typing.Union[object, typing.List[object]]:
    """Returns a decoded response payload.

    """
    # Set response payload metadata.
    try:
        typedef, is_sequence = RESPONSE_PAYLOAD_TYPE_INFO[endpoint]
    except KeyError:
        raise ValueError(f"Undefined endpoint response payload type ({endpoint})")

    if len(payload_bytes) == 0:
        return [] if is_sequence is True else None
    else:
        bytes_rem, entity = \
            codec.decode(typedef, payload_bytes, is_sequence=is_sequence)
        assert len(bytes_rem) == 0, "Unconsumed response payload bytes"
        return  entity


def _parse_response_bytes(bytes_request: bytes, bytes_response: bytes) -> bytes:
    """Parses a node's binary port response.

    """
    assert isinstance(bytes_response, bytes) is True, \
           "Response decoding error: response is not bytes"

    bytes_response_rem, length = codec.decode(U32, bytes_response)
    assert len(bytes_response_rem) == length, \
           "Response decoding error: inner byte length mismatch"

    # TODO: clarify why need to offset by 2
    assert bytes_response_rem[2:].find(bytes_request) == 0, \
           "Response decoding error: request bytes not found"

    return bytes_response
