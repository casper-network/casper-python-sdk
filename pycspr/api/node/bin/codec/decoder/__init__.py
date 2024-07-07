import typing

from pycspr.api.node.bin.codec.decoder.primitives import \
    decode_u8, \
    decode_u16, \
    decode_u32, \
    decode_u64, \
    decode_uint

from pycspr.api.node.bin.codec.decoder.domain import \
    DECODERS as _DECODERS_1
from pycspr.api.node.bin.codec.decoder.response import \
    DECODERS as _DECODERS_2


# Full decoder set.
_DECODERS: typing.Dict[typing.Type, typing.Callable] = _DECODERS_1 | _DECODERS_2


def decode(bstream: bytes, typedef: type) -> typing.Tuple[bytes, object]:
    """Decodes an entity from a byte stream.

    :param bstream: A stream of bytes.
    :param typedef: Type to be decoded.
    :returns: A decoded entity.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-decodeable type: {typedef}")
    else:
        return decoder(bstream)
