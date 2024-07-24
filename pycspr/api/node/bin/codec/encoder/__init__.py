import typing

from pycspr.api.node.bin.codec.encoder.domain import ENCODERS as _ENCODERS_DOMAIN
from pycspr.api.node.bin.codec.encoder.primitives import encode_bytes
from pycspr.api.node.bin.codec.encoder.requests_core import ENCODERS as _ENCODERS_REQUESTS_CORE
from pycspr.api.node.bin.codec.encoder.requests_get import ENCODERS as _ENCODERS_REQUESTS_GET


ENCODERS: typing.Dict[typing.Type, typing.Callable] = \
    _ENCODERS_DOMAIN | _ENCODERS_REQUESTS_CORE | _ENCODERS_REQUESTS_GET


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
