import typing

print(999)

from pycspr.api.node.bin.codec.constants import \
    ENDPOINT_TO_TAGS, \
    TAGS_TO_ENDPOINTS, \
    TAG_GET, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION
from pycspr.api.node.bin.types.core import \
    Endpoint, \
    ErrorCode, \
    Request, \
    RequestHeader, \
    Response, \
    ResponseHeader
from pycspr.api.node.bin.types.domain import \
    ProtocolVersion
from pycspr.api.node.bin.types.primitives import \
    U8x, \
    U32x, \
    U16x
from pycspr.api.node.bin.codec.utils import register_decoder, register_encoder, decode, encode


def decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, RequestHeader]:
        bytes_rem, request_version = decode(bytes_in, U16x)
        bytes_rem, protocol_version = decode(bytes_rem, ProtocolVersion)
        bytes_rem, header_tag = decode(bytes_rem, U8x)
        bytes_rem, request_id = decode(bytes_rem, U16x)

        if header_tag == TAG_TRY_ACCEPT_TRANSACTION:
            endpoint = Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            endpoint = Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_GET:
            bytes_rem, query_type = decode(bytes_rem, U8x)
            bytes_rem, query_subtype = decode(bytes_rem, U8x)
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
    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, ResponseHeader]:
        bytes_rem, protocol_version = decode(bytes_in, ProtocolVersion)
        bytes_rem, error_code = decode(bytes_rem, U16x)
        bytes_rem, response_payload_tag = decode(bytes_rem, U8x, True)

        return bytes_rem, ResponseHeader(
            protocol_version=protocol_version,
            error_code=ErrorCode(error_code),
            returned_data_type_tag=response_payload_tag
        )

    def _decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
        bytes_rem, length = decode(bytes_in, U32x)
        # TODO: why need for this offset.
        bytes_rem = bytes_rem[2:]
        bytes_rem, length = decode(bytes_rem, U32x)
        _, request = decode_request(bytes_rem[:length])

        return bytes_rem[length:], request

    bytes_rem, request = _decode_request(bytes_in)
    bytes_rem, header = _decode_header(bytes_rem)

    return b'', Response(
        bytes_raw=bytes_in,
        bytes_payload=bytes_rem,
        header=header,
        request=request
    )


def encode_request(entity: Request) -> bytes:
    def encode_header(entity: RequestHeader) -> bytes:
        return \
            encode(entity.binary_request_version, U16x) + \
            encode(entity.chain_protocol_version.major, U8x) + \
            encode(entity.chain_protocol_version.minor, U8x) + \
            encode(entity.chain_protocol_version.patch, U8x) + \
            encode(ENDPOINT_TO_TAGS[entity.endpoint][0], U8x) + \
            encode(entity.id, U16x)

    def encode_payload() -> bytes:
        print("TODO: _encode_request_payload")
        return b''

    def encode_payload_tags() -> bytes:
        return \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][1], U8x) + \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][2], U8x)

    return \
        encode_header(entity.header) + \
        encode_payload_tags() + \
        encode_payload()

register_decoder(Request, decode_request)
register_decoder(Response, decode_response)
register_encoder(Request, encode_request)
