
def le_bytes_to_int(as_bytes: bytes, signed: bool) -> int:
    """Converts a little endian byte array to an integer.

    :param as_bytes: A little endian encoded byte array integer.
    :param signed: Flag indicating whether integer is signed.

    """
    return int.from_bytes(as_bytes, byteorder='little', signed=signed)


def int_to_le_bytes(x: int, length: int, signed: bool) -> bytes:
    """Converts an integer to a little endian byte array.

    :param x: An integer to be mapped.
    :param length: Length of mapping output.
    :param signed: Flag indicating whether integer is signed.

    """
    if not isinstance(x, int):
        x = int(x)

    return bytes([i for i in x.to_bytes(length, 'little', signed=signed)])


def int_to_le_bytes_trimmed(x: int, length: int, signed: bool) -> bytes:
    """Converts an integer to a little endian byte array with trailing zeros removed.

    :param x: An integer to be mapped.
    :param length: Length of mapping output.
    :param signed: Flag indicating whether integer is signed.

    """
    value = int_to_le_bytes(x, length, signed)
    while value[-1] == 0:
        value = value[0:-1]

    return value or bytes([0])


def humanized_time_interval_to_milliseconds(interval: str) -> int:
    """Converts a human readable time interval to milliseconds.

    :param interval: A human readable time interval.
    :returns: Time interval in milliseconds.

    """
    interval = interval.lower()
    try:
        int(interval)
    except ValueError:
        ...
    else:
        return int(interval)

    if interval.endswith("ms"):
        return int(interval[0:-2])
    if interval.endswith("s"):
        return int(interval[0:-1]) * (1000)
    if interval.endswith("m"):
        return int(interval[0:-1]) * (60 * 1000)
        print("TODO: convert m")
    if interval.endswith("h"):
        return int(interval[0:-1]) * (60 * 60 * 1000)
        print("TODO: convert h")
    if interval.endswith("day"):
        return int(interval[0:-3]) * (24 * 60 * 60 * 1000)

    raise ValueError("Unsupported humanized time interval")


def milliseconds_to_humanized_time_interval(interval: int):
    """Converts milliseconds to a human readable time interval.

    :param interval: Time interval in milliseconds.
    :returns: A human readable time interval.

    """
    pass
