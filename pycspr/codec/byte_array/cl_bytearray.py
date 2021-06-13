import typing



def encode(value: typing.Union[bytes, str]) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    if isinstance(value, str):
        return [int(i) for i in bytes.fromhex(value)]    
    else:
        return [int(i) for i in value]
