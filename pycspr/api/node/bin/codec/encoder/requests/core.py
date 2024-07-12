import typing

from pycspr.api.node.bin.types.requests import \
    Request, \
    RequestHeader, \
    RequestType
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.codec.encoder.domain import \
    encode_protocol_version
from pycspr.api.node.bin.codec.encoder.requests.get import ENCODERS as _ENCODERS_1


# Set of encoders within current scope.
_ENCODERS = _ENCODERS_1


def _encode_request(entity: Request) -> bytes:
    return \
        _encode_request_header(entity.header) + \
        _encode_request_payload(entity.body)


def _encode_request_payload(entity: object) -> bytes:
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("Non-encodeable request payload.")
    else:
        return encoder(entity)


def _encode_request_header(entity: RequestHeader) -> bytes:
    return \
        encode_u16(entity.binary_request_version) + \
        encode_protocol_version(entity.chain_protocol_version) + \
        _encode_request_type(entity.type_tag) + \
        encode_u16(entity.id)


def _encode_request_type(entity: RequestType) -> bytes:
    return encode_u8(entity.value)


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: _encode_request,
    RequestHeader: _encode_request_header,
}
