import typing

from pycspr.api.node.bin.types.primitives.numeric import U32, U8

_DECODERS = dict()
_ENCODERS = dict()


def decode(
    bytes_in: bytes,
    typedef: type,
    is_optional=False,
    is_sequence=False
) -> typing.Tuple[bytes, object]:
    """Decodes an entity from a byte stream.

    :param bytes_in: A sequence of input bytes.
    :param typedef: Type to be decoded.
    :param is_optional: Flag indicating whether to apply an optionality check.
    :param is_sequence: Flag indicating whether a sequence is to be decoded.
    :returns: A decoded entity.

    """
    # Optional values are prefixed with a single byte indicating
    # whether the value is declared.
    if is_optional is True:
        bytes_rem, value = decode(bytes_in, U8)
        if value == 0:
            if is_sequence is True:
                return bytes_rem, []
            else:
                return bytes_rem, None
        elif value == 1:
            return decode(bytes_rem, typedef, is_sequence=is_sequence)
        else:
            raise ValueError("Invalid prefix bit for optional type")

    # Sequences are prefixed with sequence length.
    elif is_sequence is True:
        bytes_rem, sequence_length = decode(bytes_in, U32)
        result = []
        for _ in range(sequence_length):
            bytes_rem, entity = decode(bytes_rem, typedef, is_optional)
            result.append(entity)
        return bytes_rem, result

    # Otherwise executer decoder mapped by type.
    else:
        try:
            decoder = _DECODERS[typedef]
        except KeyError:
            raise ValueError(f"Non-decodeable type: {typedef}")
        else:
            return decoder(bytes_in)


def encode(
    entity: object,
    typedef: typing.Optional[typing.Type] = None,
    is_optional: bool = False
):
    """Encodes an entity as a byte stream.

    :param entity: Entity to be encoded.
    :param typedef: Type of entity to be encoded - typically specified for custom value types.
    :param prepend_length: Flag indicating whether to prepend byte stream length.
    :param is_optional: Flag indicating whether value is optional or not.
    :returns: A byte stream.

    """
    # Parse optional flag.
    if is_optional is True:
        if entity is None or entity == []:
            return bytes([0])
        else:
            bytes_prefix = bytes([1])
    else:
        bytes_prefix = bytes([])

    # Set type def.
    typedef = typedef or type(entity)

    # Set encoder.
    try:
        encoder = _ENCODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-encodeable type: {typedef}")

    try:
        return bytes_prefix + encoder(entity)
    except Exception as err:
        raise ValueError(f"Encoding error: {typedef} :: {err}")


def register_decoders(decoders):
    """Registers a set of encoding functions.

    :param encoders: Set of encoding functions.

    """
    for typedef, decoder in decoders:
        _DECODERS[typedef] = decoder


def register_encoders(encoders):
    """Registers a set of encoding functions.

    :param encoders: Set of encoding functions.

    """
    for typedef, encoder in encoders:
        _ENCODERS[typedef] = encoder
