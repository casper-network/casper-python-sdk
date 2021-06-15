import typing

from pycspr.codec.byte_array import cl_u8
from pycspr.codec.byte_array import cl_u32
from pycspr.codec.byte_array import cl_u64
from pycspr.codec.byte_array import cl_u128
from pycspr.codec.byte_array.utils import int_to_le_bytes_trimmed
from pycspr.types.cl import CLTypeKey


# Length when encoded.
ENCODED_LENGTH: int = 32

# Dimension constraints.
MIN = 0
MAX = (2 ** 256) - 1


def encode(value: int) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    if value < MIN or value > MAX:
        raise ValueError("Invalid U256: max size exceeded")
    
    if value >= cl_u8.MIN and value <= cl_u8.MAX:
        type_key = CLTypeKey.U8
        encoded_length = cl_u8.ENCODED_LENGTH

    elif value >= cl_u32.MIN and value <= cl_u32.MAX:
        type_key = CLTypeKey.U32
        encoded_length = cl_u32.ENCODED_LENGTH

    elif value >= cl_u64.MIN and value <= cl_u64.MAX:
        type_key = CLTypeKey.U64
        encoded_length = cl_u64.ENCODED_LENGTH

    elif value >= cl_u128.MIN and value <= cl_u128.MAX:
        type_key = CLTypeKey.U128
        encoded_length = cl_u128.ENCODED_LENGTH

    else:
        type_key = CLTypeKey.U256
        encoded_length = ENCODED_LENGTH
    
    return [type_key.value] + int_to_le_bytes_trimmed(value, encoded_length, False)
