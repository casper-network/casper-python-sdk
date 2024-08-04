import typing

from pycspr.api.node.bin.types.core import \
    Endpoint, \
    Request
from pycspr.api.node.bin.codec.constants import \
    ENDPOINT_TO_TAGS, \
    ENDPOINT_TO_TAG_BYTES, \
    TAG_GET, \
    TAG_GET_INFORMATION, \
    TAG_GET_RECORD, \
    TAG_GET_STATE, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION
from pycspr.api.node.bin.codec.primitives import \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.codec.encoder.domain import \
    encode_protocol_version


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


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: encode_request,
}
