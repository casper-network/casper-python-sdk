import typing

from pycspr.api.node.bin.codec.constants import \
    ENDPOINT_TO_TAGS, \
    ENDPOINT_TO_TAG_BYTES, \
    TAGS_TO_ENDPOINTS, \
    TAG_ENDPOINT, \
    TAG_GET, \
    TAG_GET_INFORMATION, \
    TAG_GET_RECORD, \
    TAG_GET_STATE, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION
from pycspr.api.node.bin.codec.primitives import \
    decode_u8, \
    decode_u16, \
    decode_u32, \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.codec.domain import \
    decode_protocol_version, \
    encode_protocol_version
from pycspr.api.node.bin.types.core import \
    Endpoint, \
    Request, \
    RequestHeader, \
    Response, \
    ResponseHeader


def decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    def _decode_endpoint(bytes_in: bytes, header_tag: int) -> typing.Tuple[bytes, Endpoint]:
        if header_tag == TAG_TRY_ACCEPT_TRANSACTION:
            return bytes_in, Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            return bytes_in, Endpoint.Try_AcceptTransaction
        elif header_tag == TAG_GET:
            bytes_rem, query_type = decode_u8(bytes_in)
            bytes_rem, query_subtype = decode_u8(bytes_rem)
            try:
                return bytes_rem, TAGS_TO_ENDPOINTS[(header_tag, query_type, query_subtype)]
            except KeyError:
                raise ValueError("Invalid endpoint get tag")
        raise ValueError("Invalid endpoint header tag")

    def _decode_request_payload(bytes_in: bytes, endpoint: Endpoint) -> typing.Tuple[bytes, object]:
        # TODO map endpoint to domain type.
        # TODO invoke decoder
        return b'', bytes_in

    # Header fields.
    bytes_rem, binary_request_version = decode_u16(bytes_in)
    bytes_rem, chain_protocol_version = decode_protocol_version(bytes_rem)
    bytes_rem, header_type_tag = decode_u8(bytes_rem)
    bytes_rem, request_id = decode_u16(bytes_rem)

    # Endpoint.
    bytes_rem, endpoint = _decode_endpoint(bytes_rem, header_type_tag)

    # Payload.
    bytes_rem, payload = _decode_request_payload(bytes_rem, endpoint)

    return bytes_rem, Request(
        endpoint=endpoint,
        header=RequestHeader(
            binary_request_version=binary_request_version,
            chain_protocol_version=chain_protocol_version,
            id=request_id
        ),
        payload=payload,
    )


def decode_response(bytes_in: bytes) -> typing.Tuple[bytes, Response]:
    # Destructure inner bytes.
    bytes_rem, length = decode_u32(bytes_in)

    # Decode original request.
    # TODO: why need for an offset of 2 ?
    bytes_rem = bytes_rem[2:]
    bytes_rem, length = decode_u32(bytes_rem)
    _, request = decode_request(bytes_rem[:length])

    # Decode response header.
    bytes_rem = bytes_rem[length:]
    bytes_rem, protocol_version = decode_protocol_version(bytes_rem)
    bytes_rem, error = decode_u16(bytes_rem)
    bytes_rem, returned_data_type_tag = decode_u8(bytes_rem)
    header = ResponseHeader(
        protocol_version=protocol_version,
        error=error,
        returned_data_type_tag=returned_data_type_tag
    )

    return b'', Response(
        bytes_raw=bytes_in,
        bytes_payload=bytes_rem,
        header=header,
        request=request
    )


def encode_request(entity: Request) -> bytes:
    def encode_header() -> bytes:
        return \
            encode_u16(entity.header.binary_request_version) + \
            encode_protocol_version(entity.header.chain_protocol_version) + \
            ENDPOINT_TO_TAG_BYTES[entity.endpoint][:1] + \
            encode_u16(entity.header.id)

    def encode_payload() -> bytes:
        if entity.payload is None:
            return b''

        print("TODO: _encode_request_payload")
        return b''

    def encode_payload_tag() -> bytes:
        return ENDPOINT_TO_TAG_BYTES[entity.endpoint][1:]

    return encode_header() + encode_payload_tag() + encode_payload()


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: decode_request,
    Response: decode_response,
}

ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: encode_request,
}
