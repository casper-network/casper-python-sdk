import typing

from pycspr.api.node.bin.types.primitives import U8

_DECODERS = dict()
_ENCODERS = dict()


def decode(encoded: bytes, typedef: type, is_optional=False) -> typing.Tuple[bytes, object]:
    """Decodes an entity from a byte stream.

    :param encoded: A stream of bytes.
    :param typedef: Type to be decoded.
    :returns: A decoded entity.

    """
    if is_optional is True:
        bytes_rem, value = decode(encoded, U8)
        if value == 0:
            return bytes_rem, None
        elif value == 1:
            return decode(bytes_rem, typedef)
        else:
            raise ValueError("Invalid prefix bit for optional type")
    else:
        try:
            decoder = _DECODERS[typedef]
        except KeyError:
            raise ValueError(f"Non-decodeable type: {typedef}")
        else:
            return decoder(encoded)


def encode(
    entity: object,
    typedef: typing.Type = None,
    prepend_length: bool = False,
    is_optional: bool = False
):
    """Encodes an entity as a byte stream.

    :param entity: Entity to be encoded.
    :param typedef: Type of entity to be encoded - typically specified for custom value types.
    :param prepend_length: Flag indicating whether to prepend byte stream length.
    :param is_optional: Flag indicating whether value is optional or not.
    :returns: A byte stream.

    """
    if typedef is None:
        typedef = type(entity)
    try:
        encoder = _ENCODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-encodeable type: {typedef}")

    return encode(encoder(entity), bytes) if prepend_length is True else encoder(entity)


def register_decoder(typedef: typing.Type, decoder: typing.Callable):
    """Registers a decoding function.

    :param typedef: Type of entity to be decoded.
    :param encoder: Decoding function.

    """
    _DECODERS[typedef] = decoder


def register_encoder(typedef: typing.Type, encoder: typing.Callable):
    """Registers an encoding function.

    :param typedef: Type of entity being encoded.
    :param encoder: Encoding function.

    """
    _ENCODERS[typedef] = encoder
