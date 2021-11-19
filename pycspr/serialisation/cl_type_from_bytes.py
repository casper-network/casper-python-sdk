from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes
from pycspr.types.cl import cl_types
from pycspr.types.cl import cl_values


def decode(encoded: bytes) -> cl_types.CL_Type:
    typekey = cl_types.CL_TypeKey(int(encoded[0]))

    _assert_encoded(encoded, typekey)

    try:
        return _SIMPLE_TYPES[typekey]()
    except KeyError:
        pass

    if typekey == cl_types.CL_TypeKey.BYTE_ARRAY:
        size: cl_values.CL_U32 = cl_value_from_bytes(encoded[1:], cl_types.CL_Type_U32())
        return cl_types.CL_Type_ByteArray(size.value)

    elif typekey == cl_types.CL_TypeKey.LIST:
        return cl_types.CL_Type_List(decode(encoded[1:]))

    elif typekey == cl_types.CL_TypeKey.MAP:
        raise NotImplementedError()

    elif typekey == cl_types.CL_TypeKey.OPTION:
        return cl_types.CL_Type_Option(decode(encoded[1:]))

    elif typekey == cl_types.CL_TypeKey.TUPLE_1:
        return cl_types.CL_Type_Tuple1(decode(encoded[1:]))

    elif typekey == cl_types.CL_TypeKey.TUPLE_2:
        raise NotImplementedError()

    elif typekey == cl_types.CL_TypeKey.TUPLE_3:
        raise NotImplementedError()

    else:
        raise ValueError(f"Invalid cl type byte array: {typekey}")


def _assert_encoded(encoded: bytes, typekey: cl_types.CL_TypeKey):
    if typekey in _SIMPLE_TYPES:
        assert len(encoded) == 1
    elif typekey == cl_types.CL_TypeKey.BYTE_ARRAY:
        assert len(encoded) == 5
    elif typekey == cl_types.CL_TypeKey.LIST:
        assert len(encoded) >= 2
    elif typekey == cl_types.CL_TypeKey.MAP:
        assert len(encoded) >= 3
    elif typekey == cl_types.CL_TypeKey.OPTION:
        assert len(encoded) >= 2
    elif typekey == cl_types.CL_TypeKey.TUPLE_1:
        assert len(encoded) >= 2
    elif typekey == cl_types.CL_TypeKey.TUPLE_2:
        assert len(encoded) >= 3
    elif typekey == cl_types.CL_TypeKey.TUPLE_3:
        assert len(encoded) >= 4
    else:
        assert len(encoded) > 1


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
