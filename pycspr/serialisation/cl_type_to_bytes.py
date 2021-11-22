from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.types.cl import cl_types
from pycspr.types.cl import cl_values


def encode(entity: cl_types.CL_Type) -> bytes:
    if type(entity) in _SIMPLE_TYPES:
        return bytes([entity.type_key.value])

    elif isinstance(entity, cl_types.CL_Type_ByteArray):
        return bytes([entity.type_key.value]) + cl_value_to_bytes(cl_values.CL_U32(entity.size))

    elif isinstance(entity, cl_types.CL_Type_List):
        return bytes([entity.type_key.value]) + encode(entity.inner_type)

    elif isinstance(entity, cl_types.CL_Type_Map):
        return \
            bytes([entity.type_key.value]) + \
            encode(entity.key_type) + \
            encode(entity.value_type)

    elif isinstance(entity, cl_types.CL_Type_Option):
        return bytes([entity.type_key.value]) + encode(entity.inner_type)

    elif isinstance(entity, cl_types.CL_Type_Tuple1):
        return bytes([entity.type_key.value]) + encode(entity.t0_type)

    elif isinstance(entity, cl_types.CL_Type_Tuple2):
        return bytes([entity.type_key.value]) + encode(entity.t0_type) + encode(entity.t1_type)

    elif isinstance(entity, cl_types.CL_Type_Tuple3):
        return \
            bytes([entity.type_key.value]) + \
            encode(entity.t0_type) + \
            encode(entity.t1_type) + \
            encode(entity.t2_type)


_SIMPLE_TYPES = {
    cl_types.CL_Type_Any,
    cl_types.CL_Type_Bool,
    cl_types.CL_Type_I32,
    cl_types.CL_Type_I64,
    cl_types.CL_Type_Key,
    cl_types.CL_Type_PublicKey,
    cl_types.CL_Type_Result,
    cl_types.CL_Type_String,
    cl_types.CL_Type_U8,
    cl_types.CL_Type_U32,
    cl_types.CL_Type_U64,
    cl_types.CL_Type_U128,
    cl_types.CL_Type_U256,
    cl_types.CL_Type_U512,
    cl_types.CL_Type_Unit,
    cl_types.CL_Type_URef,
}
