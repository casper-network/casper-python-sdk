import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.codec.transport.constants import \
    TAG_GET, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION, \
    TAGS_TO_ENDPOINTS
from pycspr.api.node.bin.types.chain import ProtocolVersion
from pycspr.api.node.bin.types.primitives.numeric import U8, U16, U32
from pycspr.api.node.bin.types.transport import \
    Endpoint, \
    ErrorCode, \
    Request, \
    RequestHeader, \
    Response, \
    ResponseHeader


def decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    """Decoder: sequence of bytes -> Request.

    """
    def _decode_endpoint(bytes_in: bytes, request_tag: int) -> typing.Tuple[bytes, Endpoint]:
        if request_tag == TAG_TRY_ACCEPT_TRANSACTION:
            return bytes_in, Endpoint.Try_AcceptTransaction
        elif request_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            return bytes_in, Endpoint.Try_SpeculativeExec
        elif request_tag == TAG_GET:
            bytes_out, get_type = decode(U8, bytes_in)
            bytes_out, get_subtype = decode(U8, bytes_in)
            return bytes_out, TAGS_TO_ENDPOINTS[(request_tag, get_type, get_subtype)]
        else:
            raise ValueError(f"Invalid request header tag: {request_tag}")

    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, RequestHeader]:
        bytes_out, request_version = decode(U16, bytes_in)
        bytes_out, protocol_version = decode(ProtocolVersion, bytes_out)
        bytes_out, request_tag = decode(U8, bytes_out)
        bytes_out, request_id = decode(U16, bytes_out)
        bytes_out, endpoint = _decode_endpoint(bytes_out, request_tag)

        return bytes_out, RequestHeader(request_version, protocol_version, endpoint, request_id)

    def _decode_payload(bytes_in: bytes, header: RequestHeader) -> typing.Tuple[bytes, object]:
        # TODO map endpoint to domain type.
        # TODO invoke decoder
        return b'', bytes_in

    bytes_out, header = _decode_header(bytes_in)
    bytes_out, payload = _decode_payload(bytes_out, header)

    return bytes_out, Request(header, payload)


def decode_response(bytes_in: bytes) -> typing.Tuple[bytes, Response]:
    """Decoder: sequence of bytes -> Response.

    """
    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, ResponseHeader]:
        bytes_out, protocol_version = decode(ProtocolVersion, bytes_in)
        bytes_out, error_code = decode(U16, bytes_out)
        bytes_out, response_payload_tag = decode(U8, bytes_out, True)

        return bytes_out, ResponseHeader(
            protocol_version=protocol_version,
            error_code=ErrorCode(error_code),
            returned_data_type_tag=response_payload_tag
        )

    def _decode_request_out(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
        bytes_out = bytes_in[2:]        # TODO: understand necessity for this
        bytes_out, length = decode(U32, bytes_out)
        _, request = decode_request(bytes_out[:length])

        return bytes_out[length:], request

    def _decode_response_payload(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
        bytes_out, length = decode(U32, bytes_in)
        assert(len(bytes_out) == length)

        return bytes_out, bytes_out

    bytes_out, _ = decode(U32, bytes_in)
    bytes_out, request = _decode_request_out(bytes_out)
    bytes_out, header = _decode_header(bytes_out)
    bytes_out, payload = _decode_response_payload(bytes_out)

    return b'', Response(
        bytes_raw=bytes_in,
        bytes_payload=payload,
        header=header,
        request=request
    )


register_decoders({
    (Request, decode_request),
    (Response, decode_response),
})
