import typing

from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLValue



# Decodes input data.
decode = lambda s: bool(s[0])


def encode(value: bool) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    return [int(value)]
