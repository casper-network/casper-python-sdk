import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoder
from pycspr.api.node.bin.codec.transport.constants import \
    TAG_GET, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION, \
    TAGS_TO_ENDPOINTS
from pycspr.api.node.bin.types.core import \
    Endpoint, \
    ErrorCode, \
    Request, \
    RequestHeader, \
    Response, \
    ResponseHeader
from pycspr.api.node.bin.types.domain import ProtocolVersion
from pycspr.api.node.bin.types.primitives import U8, U16, U32


def decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    """Decoder: sequence of bytes -> Request.

    """
    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, RequestHeader]:
        bytes_rem, request_version = decode(bytes_in, U16)
        bytes_rem, protocol_version = decode(bytes_rem, ProtocolVersion)
        bytes_rem, header_tag = decode(bytes_rem, U8)
        bytes_rem, request_id = decode(bytes_rem, U16)

        if header_tag == TAG_TRY_ACCEPT_TRANSACTION:
            endpoint = Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            endpoint = Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_GET:
            bytes_rem, query_type = decode(bytes_rem, U8)
            bytes_rem, query_subtype = decode(bytes_rem, U8)
            endpoint = TAGS_TO_ENDPOINTS[(header_tag, query_type, query_subtype)]
        else:
            raise ValueError("Invalid request header tag")

        return bytes_rem, RequestHeader(
            binary_request_version=request_version,
            chain_protocol_version=protocol_version,
            endpoint=endpoint,
            id=request_id
        )

    def _decode_payload(bytes_in: bytes, header: RequestHeader) -> typing.Tuple[bytes, object]:
        # TODO map endpoint to domain type.
        # TODO invoke decoder
        return b'', bytes_in

    bytes_rem, header = _decode_header(bytes_in)
    bytes_rem, payload = _decode_payload(bytes_rem, header)

    return bytes_rem, Request(header, payload)


def decode_response(bytes_in: bytes) -> typing.Tuple[bytes, Response]:
    """Decoder: sequence of bytes -> Response.

    """
    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, ResponseHeader]:
        bytes_rem, protocol_version = decode(bytes_in, ProtocolVersion)
        bytes_rem, error_code = decode(bytes_rem, U16)
        bytes_rem, response_payload_tag = decode(bytes_rem, U8, True)

        return bytes_rem, ResponseHeader(
            protocol_version=protocol_version,
            error_code=ErrorCode(error_code),
            returned_data_type_tag=response_payload_tag
        )

    def _decode_request_out(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
        bytes_rem = bytes_in[2:]        # TODO: understand necessity for this
        bytes_rem, length = decode(bytes_rem, U32)
        _, request = decode_request(bytes_rem[:length])

        return bytes_rem[length:], request

    bytes_rem, _ = decode(bytes_in, U32)
    bytes_rem, request = _decode_request_out(bytes_rem)
    bytes_rem, header = _decode_header(bytes_rem)

    return b'', Response(
        bytes_raw=bytes_in,
        bytes_payload=bytes_rem,
        header=header,
        request=request
    )


register_decoder(Request, decode_request)
register_decoder(Response, decode_response)
