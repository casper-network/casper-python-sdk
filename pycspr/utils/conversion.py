def int_to_le_bytes(x: int, length: int, signed: bool):
    """Converts an integer to a little endian byte array.

    :param x: An integer to be mapped.
    :param length: Length of mapping output.
    :param signed: Flag indicating whether integer is signed.

    """
    if not isinstance(x, int):
        x = int(x)
    return [i for i in x.to_bytes(length, 'little', signed=signed)]
    # return [0xff & x >> 8 * i for i in range(length)]


def int_to_le_bytes_trimmed(x: int, length: int, signed: bool):
    """Converts an integer to a little endian byte array with trailing zeros removed.

    :param x: An integer to be mapped.
    :param length: Length of mapping output.
    :param signed: Flag indicating whether integer is signed.

    """    
    value = int_to_le_bytes(x, length, signed)
    while value[-1] == 0:
        value = value[0:-1]
    
    return value or [0]
