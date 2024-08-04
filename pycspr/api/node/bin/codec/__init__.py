import typing

from pycspr.api.node.bin.codec.core import \
    DECODERS as _DECODERS_CORE, \
    ENCODERS as _ENCODERS_CORE
from pycspr.api.node.bin.codec.domain import \
    DECODERS as _DECODERS_DOMAIN, \
    ENCODERS as _ENCODERS_DOMAIN
from pycspr.api.node.bin.codec.requests import \
    ENCODERS as _ENCODERS_REQUESTS
from pycspr.api.node.bin.codec.primitives import \
    decode_u32, \
    encode_bytes


DECODERS: typing.Dict[typing.Type, typing.Callable] = \
    _DECODERS_CORE | _DECODERS_DOMAIN

ENCODERS: typing.Dict[typing.Type, typing.Callable] = \
    _ENCODERS_CORE | _ENCODERS_DOMAIN | _ENCODERS_REQUESTS


def decode(encoded: bytes, typedef: type) -> typing.Tuple[bytes, object]:
    """Decodes an entity from a byte stream.

    :param encoded: A stream of bytes.
    :param typedef: Type to be decoded.
    :returns: A decoded entity.

    """
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-decodeable type: {typedef}")
    else:
        return decoder(encoded)


def encode(entity: object, prepend_length: bool = False) -> bytes:
    """Encodes an entity as a byte stream.

    :param entity: Entity to be encoded.
    :param prepend_length: Flag indicating whether to prepend byte stream length.
    :returns: A byte stream.

    """
    try:
        encoder = ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Non-encodeable type: {type(entity)}")
    else:
        return encode_bytes(encoder(entity)) if prepend_length is True else encoder(entity)
