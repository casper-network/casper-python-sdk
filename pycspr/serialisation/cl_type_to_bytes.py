from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.types import cl_types
from pycspr.types import cl_values
from pycspr.types import CL_TypeKey


def encode(entity: cl_types.CL_Type) -> bytes:
    if entity.type_key in _ENCODERS_SIMPLE:
        return bytes([entity.type_key.value])
    elif entity.type_key in _ENCODERS_COMPLEX:
        return bytes([entity.type_key.value]) + _ENCODERS_COMPLEX[entity.type_key](entity)
    else:
        raise ValueError("Unrecognized cl type")


def encode_byte_array(entity: cl_types.CL_Type_ByteArray):
    return cl_value_to_bytes(cl_values.CL_U32(entity.size))


def encode_list(entity: cl_types.CL_Type_List):
    return encode(entity.inner_type)


def encode_map(entity: cl_types.CL_Type_Map):
    return encode(entity.key_type) + encode(entity.value_type)


def encode_option(entity: cl_types.CL_Type_Option):
    return encode(entity.inner_type)


def encode_tuple_1(entity: cl_types.CL_Type_Tuple1):
    return encode(entity.t0_type)


def encode_tuple_2(entity: cl_types.CL_Type_Tuple1):
    return encode(entity.t0_type) + encode(entity.t1_type)


def encode_tuple_3(entity: cl_types.CL_Type_Tuple1):
    return encode(entity.t0_type) + encode(entity.t1_type) + encode(entity.t2_type)


_ENCODERS_COMPLEX: dict = {
    CL_TypeKey.BYTE_ARRAY: encode_byte_array,
    CL_TypeKey.LIST: encode_list,
    CL_TypeKey.MAP: encode_map,
    CL_TypeKey.OPTION: encode_option,
    CL_TypeKey.TUPLE_1: encode_tuple_1,
    CL_TypeKey.TUPLE_2: encode_tuple_2,
    CL_TypeKey.TUPLE_3: encode_tuple_3,
}

_ENCODERS_SIMPLE: set = {
    CL_TypeKey.ANY,
    CL_TypeKey.BOOL,
    CL_TypeKey.I32,
    CL_TypeKey.I64,
    CL_TypeKey.KEY,
    CL_TypeKey.PUBLIC_KEY,
    CL_TypeKey.RESULT,
    CL_TypeKey.STRING,
    CL_TypeKey.U8,
    CL_TypeKey.U32,
    CL_TypeKey.U64,
    CL_TypeKey.U128,
    CL_TypeKey.U256,
    CL_TypeKey.U512,
    CL_TypeKey.UNIT,
    CL_TypeKey.UREF,
}
