import typing

from pycspr.api.node.bin.types.request import \
    Request, \
    RequestHeader, \
    RequestType, \
    RequestType_Get, \
    RequestType_Get_Information
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_u8, \
    encode_u16


def encode_request(entity: Request) -> bytes:
    return _encode_request_header(entity.header) + encode_request_body(entity.body)


def encode_request_body(entity: object) -> bytes:
    raise NotImplementedError()


def encode_request_header(entity: RequestHeader) -> bytes:
    return \
        encode_u16(entity.binary_request_version) + \
        encode(entity.chain_protocol_version) + \
        encode_request_type(entity.type_tag) + \
        encode_u16(entity.id),


def encode_request_type(entity: RequestType) -> bytes:
    return encode_u8(x.value)


def encode_request_type_get(entity: RequestType_Get) -> bytes:
    return encode_u8(x.value)


def encode_request_type_get_information(entity: RequestType_Get_Information) -> bytes:
    return encode_u8(RequestType_Get.Information.value) + encode_u8(entity.value)


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: encode_request,
    RequestHeader: encode_request_header,
    RequestType: encode_request_type,
    RequestType_Get: encode_request_type_get,
    RequestType_Get_Information: encode_request_type_get_information,
}
