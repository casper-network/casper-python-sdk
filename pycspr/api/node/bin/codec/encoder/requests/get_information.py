import typing

from pycspr.api.node.bin.codec.encoder.domain import \
    encode_block_id
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_optional, \
    encode_u8
from pycspr.api.node.bin.types.requests.core import \
    RequestType_Get, \
    RequestType_Get_Information
from pycspr.api.node.bin.types.requests.get_information import \
    GetBlockHeaderRequest, \
    GetUptimeRequest


def _encode_get_block_header_request(entity: GetBlockHeaderRequest) -> bytes:
    return \
        _encode_request_type(RequestType_Get_Information.BlockHeader) + \
        encode_optional(entity.block_id, encode_block_id)


def _encode_get_uptime_request(entity: GetUptimeRequest):
    return \
        _encode_request_type(RequestType_Get_Information.Uptime)


def _encode_request_type(entity: RequestType_Get_Information) -> bytes:
    return \
        encode_u8(RequestType_Get.Information.value) + \
        encode_u8(entity.value)


# Set of encoders within current scope.
ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    GetBlockHeaderRequest: _encode_get_block_header_request,
    GetUptimeRequest: _encode_get_uptime_request,
}
