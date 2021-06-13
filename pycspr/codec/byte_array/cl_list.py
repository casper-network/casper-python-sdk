import typing
import operator

from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLValue



def encode(value: CLValue) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    return []


# def to_bytes(instance: list, item_encoder: typing.Callable) -> bytearray:
#     return [len(instance)] + map(operator.add, [item_encoder(i) for i in instance])

