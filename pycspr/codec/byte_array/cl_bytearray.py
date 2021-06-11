import typing

from pycspr.codec.byte_array import cl_u32
from pycspr.types.cl import CLTypeKey



def encode(value: typing.Union[bytes, str]):
    """Maps a parsed value to a CL byte array representation.

    :param value: Value to be mapped.

    """
    if isinstance(value, str):
        value = bytes.fromhex(value)

    return cl_u32.encode(len(value)) + [int(i) for i in value]
