from pycspr.api.node.bin.codec.transport.constants import ENDPOINT_TO_TAGS
from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.api.node.bin.types.domain import BlockID
from pycspr.api.node.bin.types.primitives import U8, U16, U32
from pycspr.api.node.bin.types.transport.core import Request
from pycspr.api.node.bin.types.transport.requests import Get_Information_BlockHeader_RequestPayload


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
        print("TODO: _encode_request_payload")
        return encode(0, U32)

    def encode_payload_tags() -> bytes:
        return \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][1], U8) + \
            encode(ENDPOINT_TO_TAGS[entity.header.endpoint][2], U16)

    return encode_header() + encode_payload_tags() + encode_payload()


def encode_request_get_block_header(
    payload: Get_Information_BlockHeader_RequestPayload
) -> bytes:
    return encode(payload.block_id, BlockID, is_optional=True)


register_encoders({
    (Request, encode_request),
    (Get_Information_BlockHeader_RequestPayload, encode_request_get_block_header),
})
