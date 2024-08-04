import typing

from pycspr.api.node.bin.codec.decoder.domain import DECODERS as _DECODERS_DOMAIN
from pycspr.api.node.bin.codec.decoder.requests_core import DECODERS as _DECODERS_REQUESTS_CORE
from pycspr.api.node.bin.codec.decoder.responses_core import DECODERS as _DECODERS_RESPONSES_CORE


DECODERS: typing.Dict[typing.Type, typing.Callable] = \
    _DECODERS_DOMAIN | _DECODERS_REQUESTS_CORE | _DECODERS_RESPONSES_CORE


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
