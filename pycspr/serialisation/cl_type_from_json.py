import typing

from pycspr.types import cl_types


def decode(encoded: typing.Union[str, dict]) -> cl_types.CL_Type:
    """Decodes a CL type from a JSON string or object.

    :param encoded: A CL type previously encoded as JSON.
    :returns: A CL type definition.

    """    
    if isinstance(encoded, str) and encoded in _SIMPLE_TYPES:
        return _SIMPLE_TYPES[encoded]()
    elif "ByteArray" in encoded:
        return _decode_byte_array(encoded)
    elif "List" in encoded:
        return _decode_list(encoded)
    elif "Map" in encoded:
        return _decode_map(encoded)
    elif "Option" in encoded:
        return _decode_option(encoded)
    elif "Tuple1" in encoded:
        return _decode_tuple_1(encoded)
    elif "Tuple2" in encoded:
        return _decode_tuple_2(encoded)
    elif "Tuple3" in encoded:
        return _decode_tuple_3(encoded)
    else:
        raise ValueError("Invalid CL type JSON representation")


def _decode_byte_array(obj: dict):
    return cl_types.CL_Type_ByteArray(obj["ByteArray"])


def _decode_list(obj: dict):
    return cl_types.CL_Type_List(decode(obj["List"]))


def _decode_map(obj: dict):
    return cl_types.CL_Type_Map(
        decode(obj["Map"]["key"]),
        decode(obj["Map"]["value"])
        )


def _decode_option(obj: dict):
    return cl_types.CL_Type_Option(decode(obj["Option"]))


def _decode_tuple_1(obj: dict):
    return cl_types.CL_Type_Tuple1(decode(obj["Tuple1"]))


def _decode_tuple_2(obj: dict):
    return cl_types.CL_Type_Tuple2(
        decode(obj["Tuple2"][0]),
        decode(obj["Tuple2"][1])
        )


def _decode_tuple_3(obj: dict):
    return cl_types.CL_Type_Tuple3(
        decode(obj["Tuple3"][0]),
        decode(obj["Tuple3"][1]),
        decode(obj["Tuple3"][2])
        )


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
