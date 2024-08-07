import typing

from pycspr.api.node.bin.types.core import \
    Endpoint
from pycspr.api.node.bin.types.domain import \
    BlockID
from pycspr.api.node.bin.types.requests import \
    Get_Information_BlockHeader_RequestPayload
from pycspr.api.node.bin.codec.utils import encode, register_encoder


def encode_get_block_header_request(payload: Get_Information_BlockHeader_RequestPayload) -> bytes:
    return encode(payload.block_id, BlockID, is_optional=True)


register_encoder(Get_Information_BlockHeader_RequestPayload, encode_get_block_header_request)
