import typing



def encode(value: str) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    return [int(i) for i in (value or "").encode("utf-8")]
