from pycspr.api.node.bin.codec.constants import ENDPOINT_TO_TAGS
from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.type_defs.primitives import U8, U16, U32
from pycspr.api.node.bin.type_defs import Request


def encode_request(entity: Request) -> bytes:
    def encode_header() -> bytes:
        return \
            encode(entity.header.binary_request_version, U16) + \
            encode(entity.header.chain_protocol_version.major, U32) + \
            encode(entity.header.chain_protocol_version.minor, U32) + \
            encode(entity.header.chain_protocol_version.patch, U32) + \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][0], U8) + \
            encode(entity.header.id, U16)

    def encode_payload() -> bytes:
        return encode(entity.payload, bytes)

    def encode_payload_tags() -> bytes:
        # TODO: revise for Try Tx payloads which do not need these tags.
        return \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][1], U8) + \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][2], U16)

    return encode_header() + encode_payload_tags() + encode_payload()


register_encoders({
    (Request, encode_request),
})
