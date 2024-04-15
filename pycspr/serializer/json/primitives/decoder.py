import typing


def decode(typedef: object, encoded: typing.Union[dict, str]) -> object:
    """Decoder: Primitive type <- JSON blob.

    :param encoded: A JSON compatible dictionary.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(encoded)


DECODERS = {
    bool: lambda x: None if x is None else bool(x),
    bytes: lambda x: None if x is None else bytes.fromhex(x),
    dict: lambda x: x,
    int: lambda x: None if x is None else int(x),
    str: lambda x: None if x is None else x.strip(),
}
