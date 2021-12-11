from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes
from pycspr.types import cl_types


def decode(bstream: bytes) -> cl_types.CL_Type:
    """Decodes a CL type from a byte array.    

    """
    bstream, typekey = bstream[1:], cl_types.CL_TypeKey(int(bstream[0]))

    if typekey == cl_types.CL_TypeKey.BYTE_ARRAY:
        bstream, size = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
        decoded = cl_types.CL_Type_ByteArray(size.value)

    elif typekey == cl_types.CL_TypeKey.LIST:
        bstream, item_type = decode(bstream)
        decoded = cl_types.CL_Type_List(item_type)

    elif typekey == cl_types.CL_TypeKey.MAP:
        raise NotImplementedError()

    elif typekey == cl_types.CL_TypeKey.OPTION:
        bstream, option_type = decode(bstream)
        decoded = cl_types.CL_Type_Option(option_type)

    elif typekey == cl_types.CL_TypeKey.TUPLE_1:
        raise NotImplementedError()

    elif typekey == cl_types.CL_TypeKey.TUPLE_2:
        raise NotImplementedError()

    elif typekey == cl_types.CL_TypeKey.TUPLE_3:
        raise NotImplementedError()

    else:
        decoded = _SIMPLE_TYPES[typekey]()

    return bstream, decoded


_SIMPLE_TYPES = {
    cl_types.CL_TypeKey.ANY: cl_types.CL_Type_Any,
    cl_types.CL_TypeKey.BOOL: cl_types.CL_Type_Bool,
    cl_types.CL_TypeKey.I32: cl_types.CL_Type_I32,
    cl_types.CL_TypeKey.I64: cl_types.CL_Type_I64,
    cl_types.CL_TypeKey.KEY: cl_types.CL_Type_Key,
    cl_types.CL_TypeKey.PUBLIC_KEY: cl_types.CL_Type_PublicKey,
    cl_types.CL_TypeKey.RESULT: cl_types.CL_Type_Result,
    cl_types.CL_TypeKey.STRING: cl_types.CL_Type_String,
    cl_types.CL_TypeKey.U8: cl_types.CL_Type_U8,
    cl_types.CL_TypeKey.U32: cl_types.CL_Type_U32,
    cl_types.CL_TypeKey.U64: cl_types.CL_Type_U64,
    cl_types.CL_TypeKey.U128: cl_types.CL_Type_U128,
    cl_types.CL_TypeKey.U256: cl_types.CL_Type_U256,
    cl_types.CL_TypeKey.U512: cl_types.CL_Type_U512,
    cl_types.CL_TypeKey.UNIT: cl_types.CL_Type_Unit,
    cl_types.CL_TypeKey.UREF: cl_types.CL_Type_URef,
}
