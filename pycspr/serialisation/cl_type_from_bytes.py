from pycspr.types import cl_types
from pycspr.types import cl_values
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes


def decode(encoded: bytes) -> cl_types.CL_Type:
    typekey = cl_types.CL_TypeKey(int(encoded[0]))
    
    if typekey == cl_types.CL_TypeKey.ANY:
        assert len(encoded) == 1
        return cl_types.CL_Type_Any()

    elif typekey == cl_types.CL_TypeKey.BOOL:
        assert len(encoded) == 1
        return cl_types.CL_Type_Bool()

    elif typekey == cl_types.CL_TypeKey.BYTE_ARRAY:
        assert len(encoded) > 1
        size: cl_values.CL_U32 = cl_value_from_bytes(encoded[1:], cl_values.CL_U32)

        return cl_types.CL_Type_ByteArray(size.value)

