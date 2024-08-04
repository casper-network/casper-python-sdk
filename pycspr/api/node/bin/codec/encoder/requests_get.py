import typing

from pycspr.api.node.bin.codec.encoder.domain import \
    encode_block_id
from pycspr.api.node.bin.codec.primitives import \
    encode_optional, \
    encode_u8
from pycspr.api.node.bin.types.core import \
    Endpoint
from pycspr.api.node.bin.types.requests.get import \
    Get_Information_BlockHeader_RequestPayload



def encode_get_block_header_request(payload: Get_Information_BlockHeader_RequestPayload) -> bytes:
    return \
        encode_optional(payload.block_id, encode_block_id)


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Get_Information_BlockHeader_RequestPayload: encode_get_block_header_request,
}
