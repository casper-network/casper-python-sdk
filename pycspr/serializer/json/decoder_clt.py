import typing

from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLT_Any
from pycspr.types.cl import CLT_Bool
from pycspr.types.cl import CLT_ByteArray
from pycspr.types.cl import CLT_I32
from pycspr.types.cl import CLT_I64
from pycspr.types.cl import CLT_Type_U8
from pycspr.types.cl import CLT_Type_U32
from pycspr.types.cl import CLT_Type_U64
from pycspr.types.cl import CLT_Type_U128
from pycspr.types.cl import CLT_Type_U256
from pycspr.types.cl import CLT_Type_U512
from pycspr.types.cl import CLT_Type_Key
from pycspr.types.cl import CLT_Type_List
from pycspr.types.cl import CLT_Type_Map
from pycspr.types.cl import CLT_Type_Option
from pycspr.types.cl import CLT_Type_PublicKey
from pycspr.types.cl import CLT_Type_Result
from pycspr.types.cl import CLT_Type_String
from pycspr.types.cl import CLT_Type_Tuple1
from pycspr.types.cl import CLT_Type_Tuple2
from pycspr.types.cl import CLT_Type_Tuple3
from pycspr.types.cl import CLT_Type_Unit
from pycspr.types.cl import CLT_Type_URef


_SIMPLE_TYPES = {
    "Any": CLT_Any,
    "Bool": CLT_Bool,
    "I32": CLT_I32,
    "I64": CLT_I64,
    "Key": CLT_Type_Key,
    "PublicKey": CLT_Type_PublicKey,
    "Result": CLT_Type_Result,
    "String": CLT_Type_String,
    "U8": CLT_Type_U8,
    "U32": CLT_Type_U32,
    "U64": CLT_Type_U64,
    "U128": CLT_Type_U128,
    "U256": CLT_Type_U256,
    "U512": CLT_Type_U512,
    "Unit": CLT_Type_Unit,
    "URef": CLT_Type_URef,
}


def decode(encoded: typing.Union[dict, str]) -> CLT_Type:
    """Decodes a domain entity instance from JSON encoded data.

    :param encoded: JSON encoded data.
    :returns: A CL type related type instance.

    """
    if isinstance(encoded, str) and encoded in _SIMPLE_TYPES:
        return _SIMPLE_TYPES[encoded]()

    elif "ByteArray" in encoded:
        return CLT_ByteArray(
            encoded["ByteArray"]
        )

    elif "List" in encoded:
        return CLT_Type_List(
            decode(encoded["List"])
        )

    elif "Map" in encoded:
        return CLT_Type_Map(
            decode(encoded["Map"]["key"]),
            decode(encoded["Map"]["value"])
            )

    elif "Option" in encoded:
        return CLT_Type_Option(
            decode(encoded["Option"])
        )

    elif "Tuple1" in encoded:
        return CLT_Type_Tuple1(
            decode(encoded["Tuple1"])
        )

    elif "Tuple2" in encoded:
        return CLT_Type_Tuple2(
            decode(encoded["Tuple2"][0]),
            decode(encoded["Tuple2"][1])
        )

    elif "Tuple3" in encoded:
        return CLT_Type_Tuple3(
            decode(encoded["Tuple3"][0]),
            decode(encoded["Tuple3"][1]),
            decode(encoded["Tuple3"][2])
            )

    else:
        raise ValueError("Invalid CL type JSON representation")
