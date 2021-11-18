import typing
from pycspr.types import cl_types


def decode(encoded: typing.Union[str, dict]) -> cl_types.CL_Type:
    if "Any" == encoded:
        return cl_types.CL_Type_Any()
    elif "Bool" == encoded:
        return cl_types.CL_Type_Bool()
    elif "ByteArray" in encoded:
        return cl_types.CL_Type_ByteArray(encoded["ByteArray"])
    elif "I32" == encoded:
        return cl_types.CL_Type_I32()
    elif "I64" == encoded:
        return cl_types.CL_Type_I64()
    elif "Key" == encoded:
        return cl_types.CL_Type_Key()
    elif "List" in encoded:
        return cl_types.CL_Type_List(decode(encoded["List"]))
    elif "Map" in encoded:
        raise NotImplementedError()
    elif "Option" in encoded:
        return cl_types.CL_Type_Option(decode(encoded["Option"]))
    elif "PublicKey" == encoded:
        return cl_types.CL_Type_PublicKey()
    elif "Result" in encoded:
        return cl_types.CL_Type_Result()
    elif "String" == encoded:
        return cl_types.CL_Type_String()
    elif "Tuple1" in encoded:
        return cl_types.CL_Type_Tuple1(decode(encoded["Tuple1"]))
    elif "Tuple2" in encoded:
        return cl_types.CL_Type_Tuple2(decode(encoded["Tuple2"][0]), decode(encoded["Tuple2"][1]))
    elif "Tuple3" in encoded:
        return cl_types.CL_Type_Tuple3(decode(encoded["Tuple3"][0]), decode(encoded["Tuple3"][1]), decode(encoded["Tuple3"][2]))
    elif "U8" == encoded:
        return cl_types.CL_Type_U8()
    elif "U32" == encoded:
        return cl_types.CL_Type_U32()
    elif "U64" == encoded:
        return cl_types.CL_Type_U64()
    elif "U128" == encoded:
        return cl_types.CL_Type_U128()
    elif "U256" == encoded:
        return cl_types.CL_Type_U256()
    elif "U512" == encoded:
        return cl_types.CL_Type_U512()
    elif "Unit" == encoded:
        return cl_types.CL_Type_Unit()
    elif "URef" == encoded:
        return cl_types.CL_Type_URef()

    raise ValueError("Invalid CL type JSON representation")
