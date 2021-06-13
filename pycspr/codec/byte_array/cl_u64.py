import typing

from pycspr.codec.byte_array import cl_u32
from pycspr.codec.byte_array.utils import int_to_le_bytes
from pycspr.types.cl import CLValue


# Length when encoded.
_ENCODED_LENGTH: int = 8

# Dimension constraints.
MIN = 0
MAX = (2 ** 64) - 1



def encode(value: int) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    return int_to_le_bytes(value, _ENCODED_LENGTH, False)
