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


def _decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    """Decoder: sequence of bytes -> Request.

    """
    def _decode_endpoint(bytes_in: bytes, request_tag: int) -> typing.Tuple[bytes, Endpoint]:
        if request_tag == TAG_TRY_ACCEPT_TRANSACTION:
            return bytes_in, Endpoint.Try_AcceptTransaction
        elif request_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            return bytes_in, Endpoint.Try_SpeculativeExec
        elif request_tag == TAG_GET:
            bytes_rem, get_type = decode(U8, bytes_in)
            bytes_rem, get_subtype = decode(U8, bytes_in)
            return bytes_rem, TAGS_TO_ENDPOINTS[(request_tag, get_type, get_subtype)]
        else:
            raise ValueError(f"Invalid request header tag: {request_tag}")

    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, RequestHeader]:
        bytes_rem, request_version = decode(U16, bytes_in)
        bytes_rem, protocol_version = decode(ProtocolVersion, bytes_rem)
        bytes_rem, request_tag = decode(U8, bytes_rem)
        bytes_rem, request_id = decode(U16, bytes_rem)
        bytes_rem, endpoint = _decode_endpoint(bytes_rem, request_tag)

        return bytes_rem, RequestHeader(request_version, protocol_version, endpoint, request_id)

    def _decode_payload(bytes_in: bytes, header: RequestHeader) -> typing.Tuple[bytes, object]:
        # TODO map endpoint to domain type.
        # TODO invoke decoder
        return b'', bytes_in

    bytes_rem, header = _decode_header(bytes_in)
    bytes_rem, payload = _decode_payload(bytes_rem, header)

    return bytes_rem, Request(header, payload)


def _decode_response(bytes_in: bytes) -> typing.Tuple[bytes, Response]:
    """Decoder: sequence of bytes -> Response.

    """
    def _decode_response_header(bytes_in: bytes) -> typing.Tuple[bytes, ResponseHeader]:
        bytes_rem, protocol_version = decode(ProtocolVersion, bytes_in)
        bytes_rem, error_code = decode(U16, bytes_rem)
        bytes_rem, response_payload_tag = decode(U8, bytes_rem, True)

        return bytes_rem, ResponseHeader(
            protocol_version=protocol_version,
            error_code=ErrorCode(error_code),
            returned_data_type_tag=response_payload_tag
        )

    def _decode_request_out(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
        bytes_rem = bytes_in[2:]        # TODO: understand necessity for this
        bytes_rem, length = decode(U32, bytes_rem)
        _, request = _decode_request(bytes_rem[:length])

        return bytes_rem[length:], request

    def _decode_response_payload_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
        bytes_rem, size = decode(U32, bytes_in)
        assert(len(bytes_rem) == size)

        return bytes_rem, bytes_rem

    bytes_rem, _ = decode(U32, bytes_in)
    bytes_rem, request = _decode_request_out(bytes_rem)
    bytes_rem, header = _decode_response_header(bytes_rem)
    bytes_rem, bytes_payload = _decode_response_payload_bytes(bytes_rem)

    return b'',  Response(
        bytes_raw=bytes_in,
        header=header,
        bytes_payload=bytes_payload,
        request=request
    )


register_decoders({
    (Request, _decode_request),
    (Response, _decode_response),
})
