from pycspr.api.node.bin.codec.utils import encode, register_encoder
from pycspr.api.node.bin.types.domain import BlockID
from pycspr.api.node.bin.types.requests import Get_Information_BlockHeader_RequestPayload


def _encode_get_block_header_request(
    payload: Get_Information_BlockHeader_RequestPayload
) -> bytes:
    return encode(payload.block_id, BlockID, is_optional=True)


register_encoder(
    Get_Information_BlockHeader_RequestPayload,
    _encode_get_block_header_request
)
