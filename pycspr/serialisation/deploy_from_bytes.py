def decode(bstream: bytes, typedef: object) -> object:
    """Decodes a deploy from a byte array.

    :param bstream: An array of bytes being decoded.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """ 
    raise NotImplementedError(typedef, bstream)
