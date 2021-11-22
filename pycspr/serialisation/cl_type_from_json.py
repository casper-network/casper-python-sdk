import typing

from pycspr.types.cl import cl_types


def decode(encoded: typing.Union[str, dict]) -> cl_types.CL_Type:
    # Simple types.
    if isinstance(encoded, str):
        try:
            return _SIMPLE_TYPES[encoded]()
        except KeyError:
            pass

    # Complex types.
    if "ByteArray" in encoded:
        return cl_types.CL_Type_ByteArray(encoded["ByteArray"])

    elif "List" in encoded:
        return cl_types.CL_Type_List(decode(encoded["List"]))

    elif "Map" in encoded:
        return cl_types.CL_Type_Map(
            decode(encoded["Map"]["key"]),
            decode(encoded["Map"]["value"])
            )

    elif "Option" in encoded:
        return cl_types.CL_Type_Option(decode(encoded["Option"]))

    elif "Tuple1" in encoded:
        return cl_types.CL_Type_Tuple1(decode(encoded["Tuple1"]))

    elif "Tuple2" in encoded:
        return cl_types.CL_Type_Tuple2(
            decode(encoded["Tuple2"][0]),
            decode(encoded["Tuple2"][1])
            )

    elif "Tuple3" in encoded:
        return cl_types.CL_Type_Tuple3(
            decode(encoded["Tuple3"][0]),
            decode(encoded["Tuple3"][1]),
            decode(encoded["Tuple3"][2])
            )

    else:
        raise ValueError("Invalid CL type JSON representation")


_SIMPLE_TYPES = {
    "Any": cl_types.CL_Type_Any,
    "Bool": cl_types.CL_Type_Bool,
    "I32": cl_types.CL_Type_I32,
    "I64": cl_types.CL_Type_I64,
    "Key": cl_types.CL_Type_Key,
    "PublicKey": cl_types.CL_Type_PublicKey,
    "Result": cl_types.CL_Type_Result,
    "String": cl_types.CL_Type_String,
    "U8": cl_types.CL_Type_U8,
    "U32": cl_types.CL_Type_U32,
    "U64": cl_types.CL_Type_U64,
    "U128": cl_types.CL_Type_U128,
    "U256": cl_types.CL_Type_U256,
    "U512": cl_types.CL_Type_U512,
    "Unit": cl_types.CL_Type_Unit,
    "URef": cl_types.CL_Type_URef,
}
