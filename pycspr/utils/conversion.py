import typing



def le_bytes_to_int(as_bytes: typing.List[int], signed: bool) -> int:
    """Converts a little endian byte array to an integer.

    :param as_bytes: A little endian encoded byte array integer.
    :param signed: Flag indicating whether integer is signed.

    """
    return int.from_bytes(as_bytes, byteorder='little', signed=signed)    


def int_to_le_bytes(x: int, length: int, signed: bool) -> typing.List[int]:
    """Converts an integer to a little endian byte array.

    :param x: An integer to be mapped.
    :param length: Length of mapping output.
    :param signed: Flag indicating whether integer is signed.

    """
    if not isinstance(x, int):
        x = int(x)
    return [i for i in x.to_bytes(length, 'little', signed=signed)]


def int_to_le_bytes_trimmed(x: int, length: int, signed: bool) -> typing.List[int]:
    """Converts an integer to a little endian byte array with trailing zeros removed.

    :param x: An integer to be mapped.
    :param length: Length of mapping output.
    :param signed: Flag indicating whether integer is signed.

    """    
    value = int_to_le_bytes(x, length, signed)
    while value[-1] == 0:
        value = value[0:-1]
    
    return value or [0]
