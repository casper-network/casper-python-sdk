import typing

from pycspr.api.node.bin.types.request import \
    Request, \
    RequestHeader, \
    RequestType
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.codec.encoder.domain import \
    encode_protocol_version
from pycspr.api.node.bin.codec.encoder.request_get_information import \
    ENCODERS as _ENCODERS_1
from pycspr.api.node.bin.codec.encoder.request_get_record import \
    ENCODERS as _ENCODERS_2
from pycspr.api.node.bin.codec.encoder.request_get_state import \
    ENCODERS as _ENCODERS_3

_ENCODERS = _ENCODERS_1 | _ENCODERS_2 | _ENCODERS_3


def encode_request(entity: Request) -> bytes:
    return \
        encode_request_header(entity.header) + \
        encode_request_body(entity.body)


def encode_request_body(entity: object) -> bytes:
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("Non-encodeable request body.")
    else:
        return encoder(entity)


def encode_request_header(entity: RequestHeader) -> bytes:
    return \
        encode_u16(entity.binary_request_version) + \
        encode_protocol_version(entity.chain_protocol_version) + \
        encode_request_type(entity.type_tag) + \
        encode_u16(entity.id)


def encode_request_type(entity: RequestType) -> bytes:
    return encode_u8(entity.value)


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: encode_request,
    RequestHeader: encode_request_header,
    RequestType: encode_request_type,
}
