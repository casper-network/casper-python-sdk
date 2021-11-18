from pycspr.serialisation.cl_type_from_json import decode as cl_type_from_json
from pycspr.types import cl_types
from pycspr.types import cl_values


def decode(encoded: dict):
    cl_type: cl_types.CL_Type = cl_type_from_json(encoded["cl_type"])
    cl_value_type: cl_values.CL_Value = _get_cl_value_type(cl_type)

    return cl_value_type.from_bytes(encoded["bytes"])


def _get_cl_value_type(cl_type: cl_types.CL_Type):
    if isinstance(cl_type, cl_types.CL_Type_Any):
        return cl_values.CL_Any
    elif isinstance(cl_type, cl_types.CL_Type_Bool):
        return cl_values.CL_Bool
    elif isinstance(cl_type, cl_types.CL_Type_ByteArray):
        return cl_values.CL_ByteArray
    elif isinstance(cl_type, cl_types.CL_Type_I32):
        return cl_values.CL_I32
    elif isinstance(cl_type, cl_types.CL_Type_I64):
        return cl_values.CL_I64
    elif isinstance(cl_type, cl_types.CL_Type_Key):
        return cl_values.CL_Key
    elif isinstance(cl_type, cl_types.CL_Type_List):
        return cl_values.CL_List
    elif isinstance(cl_type, cl_types.CL_Type_Map):
        return cl_values.CL_Map
    elif isinstance(cl_type, cl_types.CL_Type_Option):
        return cl_values.CL_Option
    elif isinstance(cl_type, cl_types.CL_Type_PublicKey):
        return cl_values.CL_PublicKey
    elif isinstance(cl_type, cl_types.CL_Type_Result):
        return cl_values.CL_Result
    elif isinstance(cl_type, cl_types.CL_Type_String):
        return cl_values.CL_String
    elif isinstance(cl_type, cl_types.CL_Type_Tuple1):
        return cl_values.CL_Tuple1
    elif isinstance(cl_type, cl_types.CL_Type_Tuple2):
        return cl_values.CL_Tuple2
    elif isinstance(cl_type, cl_types.CL_Type_Tuple3):
        return cl_values.CL_Tuple3
    elif isinstance(cl_type, cl_types.CL_Type_U8):
        return cl_values.CL_U8
    elif isinstance(cl_type, cl_types.CL_Type_U32):
        return cl_values.CL_U32
    elif isinstance(cl_type, cl_types.CL_Type_U64):
        return cl_values.CL_U64
    elif isinstance(cl_type, cl_types.CL_Type_U128):
        return cl_values.CL_U128
    elif isinstance(cl_type, cl_types.CL_Type_U256):
        return cl_values.CL_U256
    elif isinstance(cl_type, cl_types.CL_Type_U512):
        return cl_values.CL_U512
    elif isinstance(cl_type, cl_types.CL_Type_Unit):
        return cl_values.CL_Unit
    elif isinstance(cl_type, cl_types.CL_Type_URef):
        return cl_values.CL_URef
    else:
        raise ValueError(f"CL type ({cl_type}) cannot be mapped to a CL value type")
