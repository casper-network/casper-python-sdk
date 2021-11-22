import typing

from pycspr.types.cl import cl_types


def encode(entity: cl_types.CL_Type) -> typing.Union[str, dict]:
    # Simple types are mapped to a string.
    try:
        return _SIMPLE_TYPES[type(entity)]
    except KeyError:
        pass

    # Complex types are mapped to a dict.
    if isinstance(entity, cl_types.CL_Type_ByteArray):
        return {
            "ByteArray": entity.size
        }
    elif isinstance(entity, cl_types.CL_Type_List):
        return {
            "List": encode(entity.inner_type)
        }
    elif isinstance(entity, cl_types.CL_Type_Map):
        return {
            "Map": {
                "key": encode(entity.key_type),
                "value": encode(entity.value_type)
            }
        }
    elif isinstance(entity, cl_types.CL_Type_Option):
        return {
            "Option": encode(entity.inner_type)
        }
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


_SIMPLE_TYPES = {
    cl_types.CL_Type_Any: "Any",
    cl_types.CL_Type_Bool: "Bool",
    cl_types.CL_Type_I32: "I32",
    cl_types.CL_Type_I64: "I64",
    cl_types.CL_Type_Key: "Key",
    cl_types.CL_Type_PublicKey: "PublicKey",
    cl_types.CL_Type_Result: "Result",
    cl_types.CL_Type_String: "String",
    cl_types.CL_Type_U8: "U8",
    cl_types.CL_Type_U32: "U32",
    cl_types.CL_Type_U64: "U64",
    cl_types.CL_Type_U128: "U128",
    cl_types.CL_Type_U256: "U256",
    cl_types.CL_Type_U512: "U512",
    cl_types.CL_Type_Unit: "Unit",
    cl_types.CL_Type_URef: "URef"
}
