import typing

from pycspr.api.node.bin.codec.encoder import ENCODERS
from pycspr.api.node.bin.codec.encoder.primitives import encode_u32
from pycspr.api.node.bin.codec.decoder import DECODERS
from pycspr.api.node.bin.codec.decoder.primitives import decode_u32


def decode(bstream: bytes, typedef: type) -> typing.Tuple[bytes, object]:
    """Decodes an entity from a byte stream.

    :param bstream: A stream of bytes.
    :param typedef: Type to be decoded.
    :returns: A decoded entity.

    """
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-decodeable type: {typedef}")
    else:
        return decoder(bstream)


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
        bstream: bytes = encoder(entity)
        return \
            bstream if prepend_length is False else \
            encode_u32(len(bstream)) + bstream
