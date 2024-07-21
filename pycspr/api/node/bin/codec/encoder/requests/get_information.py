import typing

from pycspr.api.node.bin.codec.encoder.domain import \
    encode_block_id
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_optional, \
    encode_u8
from pycspr.api.node.bin.types.requests.core import \
    Endpoint
from pycspr.api.node.bin.types.requests.get_information import \
    GetBlockHeaderRequestPayload



def encode_get_block_header_request(entity: GetBlockHeaderRequestPayload) -> bytes:
    return \
        encode_request_type_1(Endpoint.Get_Information_BlockHeader) + \
        encode_optional(entity.block_id, encode_block_id)



# Set of encoders within current scope.
ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    GetBlockHeaderRequestPayload: encode_get_block_header_request,
}
