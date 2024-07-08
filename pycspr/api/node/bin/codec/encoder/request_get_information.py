import typing

from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_optional
from pycspr.api.node.bin.codec.encoder.request_core import \
    encode_request_type_get_information
from pycspr.api.node.bin.types.request import \
    RequestType_Get_Information
from pycspr.api.node.bin.types.request.get_information import \
    GetBlockHeaderRequest, \
    GetUptimeRequest


def encode_get_block_header_request(entity: GetBlockHeaderRequest):
    return \
        encode_request_type_get_information(RequestType_Get_Information.BlockHeader), \
        encode_optional(entity.block_id, encode_block_id),


def encode_get_uptime_request(entity: GetUptimeRequest):
    return \
        encode_request_type_get_information(RequestType_Get_Information.Uptime)


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    GetBlockHeaderRequest: encode_get_block_header_request,
    GetUptimeRequest: encode_get_uptime_request,
}
