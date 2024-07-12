import typing

from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_u8
from pycspr.api.node.bin.types.requests.core import \
    RequestType_Get, \
    RequestType_Get_Record


def _encode_request_type(entity: RequestType_Get_Record) -> bytes:
    return \
        encode_u8(RequestType_Get.Record.value) + \
        encode_u8(entity.value)


# Set of encoders within current scope.
ENCODERS: typing.Dict[typing.Type, typing.Callable] = {}
