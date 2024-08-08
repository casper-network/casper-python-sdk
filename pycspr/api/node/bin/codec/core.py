import typing

from pycspr.api.node.bin.codec import utils
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
from pycspr.api.node.bin.types.domain import ProtocolVersion
from pycspr.api.node.bin.types.primitives import U8, U32, U16


def decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, RequestHeader]:
        bytes_rem, request_version = utils.decode(bytes_in, U16)
        bytes_rem, protocol_version = utils.decode(bytes_rem, ProtocolVersion)
        bytes_rem, header_tag = utils.decode(bytes_rem, U8)
        bytes_rem, request_id = utils.decode(bytes_rem, U16)

        if header_tag == TAG_TRY_ACCEPT_TRANSACTION:
            endpoint = Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            endpoint = Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_GET:
            bytes_rem, query_type = utils.decode(bytes_rem, U8)
            bytes_rem, query_subtype = utils.decode(bytes_rem, U8)
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
        bytes_rem, protocol_version = utils.decode(bytes_in, ProtocolVersion)
        bytes_rem, error_code = utils.decode(bytes_rem, U16)
        bytes_rem, response_payload_tag = utils.decode(bytes_rem, U8, True)

        return bytes_rem, ResponseHeader(
            protocol_version=protocol_version,
            error_code=ErrorCode(error_code),
            returned_data_type_tag=response_payload_tag
        )

    def _decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
        bytes_rem, length = utils.decode(bytes_in, U32)
        # TODO: why need for this offset.
        bytes_rem = bytes_rem[2:]
        bytes_rem, length = utils.decode(bytes_rem, U32)
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
            utils.encode(entity.binary_request_version, U16) + \
            utils.encode(entity.chain_protocol_version.major, U8) + \
            utils.encode(entity.chain_protocol_version.minor, U8) + \
            utils.encode(entity.chain_protocol_version.patch, U8) + \
            utils.encode(ENDPOINT_TO_TAGS[entity.endpoint][0], U8) + \
            utils.encode(entity.id, U16)

    def encode_payload() -> bytes:
        print("TODO: _encode_request_payload")
        return b''

    def encode_payload_tags() -> bytes:
        return \
            utils.encode(ENDPOINT_TO_TAGS[entity.header.endpoint][1], U8) + \
            utils.encode(ENDPOINT_TO_TAGS[entity.header.endpoint][2], U8)

    return \
        encode_header(entity.header) + \
        encode_payload_tags() + \
        encode_payload()

utils.register_decoder(Request, decode_request)
utils.register_decoder(Response, decode_response)
utils.register_encoder(Request, encode_request)
