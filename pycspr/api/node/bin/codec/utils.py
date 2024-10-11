import typing

from pycspr.api.node.bin.types.primitives.numeric import U32, U8

_DECODERS = dict()
_ENCODERS = dict()


# Targets
# Map: T` <-> T`
# Seq: T
# T: simple | complex

def decode(
    typedef: typing.Union[type, typing.Tuple[type, type]],
    bytes_in: bytes,
    is_optional=False,
    is_sequence=False,
) -> typing.Tuple[bytes, object]:
    """Decodes an entity from a byte stream.

    :param typedef: Type to be decoded.
    :param bytes_in: A sequence of input bytes.
    :param is_optional: Flag indicating whether to apply an optionality check.
    :param is_sequence: Flag indicating whether a sequence is to be decoded.
    :returns: A decoded entity.

    """
    # Maps are passed as 2 member tuple.
    is_map = isinstance(typedef, tuple)
    if is_map:
        if len(typedef) != 2:
            raise ValueError("Invalid map declaration")

    # Zero bytes are mapped to defaults.
    if bytes_in == bytes([]):
        if is_map is True:
            return bytes([]), dict()
        elif typedef is bytes:
            return bytes([]), bytes([])
        elif is_sequence is True:
            return bytes([]), []
        else:
            return bytes([]), None

    # Optional values are prefixed with a single byte predicate.
    if is_optional is True:
        bytes_rem, value = decode(U8, bytes_in)
        if value == 0:
            if is_map is True:
                return bytes_rem, dict()
            elif typedef is bytes:
                return bytes_rem, bytes([])
            elif is_sequence is True:
                return bytes_rem, []
            else:
                return bytes_rem, None
        elif value == 1:
            return decode(typedef, bytes_rem, is_sequence=is_sequence)
        else:
            raise ValueError("Invalid prefix bit for optional type")

    if is_map == True:
        assert is_optional == False, "Optionality cannot apply to a mapping"
        (K, V) = typedef
        rem, size = decode(U32, bytes_in)
        result = dict()
        for idx in range(size):
            rem, key = decode(K, rem)
            rem, value = decode(V, rem)
            result[key] = value
        return rem, result

    # Sequences are prefixed with sequence length.
    if is_sequence is True:
        bytes_rem, size = decode(U32, bytes_in)
        result = []
        for _ in range(size):
            bytes_rem, entity = decode(typedef, bytes_rem, is_optional)
            result.append(entity)
        return bytes_rem, result

    # Otherwise invoke type decoder.
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


def register_decoders(decoders: typing.List[typing.Tuple[type, typing.Callable]]):
    """Registers a set of encoding functions.

    :param encoders: Set of encoding functions.

    """
    for typedef, decoder in decoders:
        _DECODERS[typedef] = decoder


def register_encoders(encoders: typing.List[typing.Tuple[type, typing.Callable]]):
    """Registers a set of encoding functions.

    :param encoders: Set of encoding functions.

    """
    for typedef, encoder in encoders:
        _ENCODERS[typedef] = encoder
