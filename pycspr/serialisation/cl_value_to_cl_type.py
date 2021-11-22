from pycspr.types.cl import cl_types
from pycspr.types.cl import cl_values


def encode(entity: cl_values.CL_Value) -> cl_types.CL_Type:
    if isinstance(entity, cl_values.CL_Any):
        return cl_types.CL_Type_Any()

    elif isinstance(entity, cl_values.CL_Bool):
        return cl_types.CL_Type_Bool()

    elif isinstance(entity, cl_values.CL_ByteArray):
        return cl_types.CL_Type_ByteArray(len(entity))

    elif isinstance(entity, cl_values.CL_I32):
        return cl_types.CL_Type_I32()

    elif isinstance(entity, cl_values.CL_I64):
        return cl_types.CL_Type_I64()

    elif isinstance(entity, cl_values.CL_Key):
        return cl_types.CL_Type_Key()

    elif isinstance(entity, cl_values.CL_List):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Map):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Option):
        return cl_types.CL_Type_Option(entity.option_type)

    elif isinstance(entity, cl_values.CL_PublicKey):
        return cl_types.CL_Type_PublicKey()

    elif isinstance(entity, cl_values.CL_Result):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_String):
        return cl_types.CL_Type_String()

    elif isinstance(entity, cl_values.CL_Tuple1):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Tuple2):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Tuple3):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_U8):
        return cl_types.CL_Type_U8()

    elif isinstance(entity, cl_values.CL_U32):
        return cl_types.CL_Type_U32()

    elif isinstance(entity, cl_values.CL_U64):
        return cl_types.CL_Type_U64()

    elif isinstance(entity, cl_values.CL_U128):
        return cl_types.CL_Type_U128()

    elif isinstance(entity, cl_values.CL_U256):
        return cl_types.CL_Type_U256()

    elif isinstance(entity, cl_values.CL_U512):
        return cl_types.CL_Type_U512()

    elif isinstance(entity, cl_values.CL_Unit):
        return cl_types.CL_Type_Unit()

    elif isinstance(entity, cl_values.CL_URef):
        return cl_types.CL_Type_URef()

    else:
        raise ValueError("CL value cannot be encoded as CL type")
