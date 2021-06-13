import typing

from pycspr.codec.byte_array.utils import int_to_le_bytes



# Length when encoded.
_ENCODED_LENGTH: int = 8


def encode(value: int) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    return int_to_le_bytes(value, _ENCODED_LENGTH, False)
