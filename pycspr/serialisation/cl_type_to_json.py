import typing
from pycspr.types import cl_types


def encode(entity: cl_types.CL_Type) -> typing.Union[str, dict]:
    if isinstance(entity, cl_types.CL_Type_Any):
        return "Any"
    elif isinstance(entity, cl_types.CL_Type_Bool):
        return "Bool"
    elif isinstance(entity, cl_types.CL_Type_ByteArray):
        return {
            "ByteArray": entity.size
        }
    elif isinstance(entity, cl_types.CL_Type_I32):
        return "I32"
    elif isinstance(entity, cl_types.CL_Type_I64):
        return "I64"
    elif isinstance(entity, cl_types.CL_Type_Key):
        return "Key"
    elif isinstance(entity, cl_types.CL_Type_List):
        return {
            "List": encode(entity.inner_type)
        }
    elif isinstance(entity, cl_types.CL_Type_Map):
        raise NotImplementedError()
    elif isinstance(entity, cl_types.CL_Type_Option):
        return {
            "Option": encode(entity.inner_type)
        }
    elif isinstance(entity, cl_types.CL_Type_PublicKey):
        return "PublicKey"
    elif isinstance(entity, cl_types.CL_Type_Result):
        return "Result"
    elif isinstance(entity, cl_types.CL_Type_String):
        return "String"
    elif isinstance(entity, cl_types.CL_Type_U8):
        return "U8"
    elif isinstance(entity, cl_types.CL_Type_U32):
        return "U32"
    elif isinstance(entity, cl_types.CL_Type_U64):
        return "U64"
    elif isinstance(entity, cl_types.CL_Type_U128):
        return "U128"
    elif isinstance(entity, cl_types.CL_Type_U256):
        return "U256"
    elif isinstance(entity, cl_types.CL_Type_U512):
        return "U512"
    elif isinstance(entity, cl_types.CL_Type_Tuple1):
        return {
            "Tuple1": encode(entity.t0_type)
        }
    elif isinstance(entity, cl_types.CL_Type_Tuple2):
        return {
            "Tuple2": [
                encode(entity.t0_type),
                encode(entity.t1_type),
            ]
        }
    elif isinstance(entity, cl_types.CL_Type_Tuple3):
        return {
            "Tuple3": [
                encode(entity.t0_type),
                encode(entity.t1_type),
                encode(entity.t2_type)
            ]
        }
    elif isinstance(entity, cl_types.CL_Type_Unit):
        return "Unit"
    elif isinstance(entity, cl_types.CL_Type_URef):
        return "URef"
