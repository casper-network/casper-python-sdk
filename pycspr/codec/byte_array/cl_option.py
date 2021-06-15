import typing

from pycspr.types.cl import CLValue
from pycspr import factory



def encode(value: CLValue) -> typing.List[int]:
    """Maps parsed value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    # JIT import so as to avoid circular references.
    from pycspr.codec import byte_array

    if value.parsed is None:
        return [0]
    else:
        return [1] + \
            byte_array.encode(
                factory.cl_types.create_value(
                    value.cl_type.inner_type,
                    value.parsed
                    )
                )
