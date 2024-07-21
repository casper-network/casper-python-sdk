import typing

from pycspr.api.node.bin.codec.decoder.domain import DECODERS as _DECODERS_1
from pycspr.api.node.bin.codec.decoder.requests import DECODERS as _DECODERS_2
from pycspr.api.node.bin.codec.decoder.responses import DECODERS as _DECODERS_3


DECODERS: typing.Dict[typing.Type, typing.Callable] = _DECODERS_1 | _DECODERS_2 | _DECODERS_3


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
