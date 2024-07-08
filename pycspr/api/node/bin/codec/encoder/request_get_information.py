import typing

from pycspr.api.node.bin.codec.encoder.domain import \
    encode_block_id
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_optional, \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.types.request import \
    RequestType_Get, \
    RequestType_Get_Information
from pycspr.api.node.bin.types.request.get_information import \
    GetBlockHeaderRequest, \
    GetUptimeRequest


def encode_get_block_header_request(entity: GetBlockHeaderRequest) -> bytes:
    return \
        encode_request_type(RequestType_Get_Information.BlockHeader) + \
        encode_optional(entity.block_id, encode_block_id)


def encode_request_type(entity: RequestType_Get_Information) -> bytes:
    return \
        encode_u8(RequestType_Get.Information.value) + \
        encode_u8(entity.value)


def encode_get_uptime_request(entity: GetUptimeRequest):
    return \
        encode_request_type(RequestType_Get_Information.Uptime)


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    GetBlockHeaderRequest: encode_get_block_header_request,
    GetUptimeRequest: encode_get_uptime_request,
    RequestType_Get_Information: encode_request_type,
}
