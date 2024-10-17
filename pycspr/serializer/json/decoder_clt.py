import typing

from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.cl_types import CLT_Any
from pycspr.type_defs.cl_types import CLT_Bool
from pycspr.type_defs.cl_types import CLT_ByteArray
from pycspr.type_defs.cl_types import CLT_I32
from pycspr.type_defs.cl_types import CLT_I64
from pycspr.type_defs.cl_types import CLT_U8
from pycspr.type_defs.cl_types import CLT_U32
from pycspr.type_defs.cl_types import CLT_U64
from pycspr.type_defs.cl_types import CLT_U128
from pycspr.type_defs.cl_types import CLT_U256
from pycspr.type_defs.cl_types import CLT_U512
from pycspr.type_defs.cl_types import CLT_Key
from pycspr.type_defs.cl_types import CLT_List
from pycspr.type_defs.cl_types import CLT_Map
from pycspr.type_defs.cl_types import CLT_Option
from pycspr.type_defs.cl_types import CLT_PublicKey
from pycspr.type_defs.cl_types import CLT_Result
from pycspr.type_defs.cl_types import CLT_String
from pycspr.type_defs.cl_types import CLT_Tuple1
from pycspr.type_defs.cl_types import CLT_Tuple2
from pycspr.type_defs.cl_types import CLT_Tuple3
from pycspr.type_defs.cl_types import CLT_Unit
from pycspr.type_defs.cl_types import CLT_URef


_SIMPLE_TYPES = {
    "Any": CLT_Any,
    "Bool": CLT_Bool,
    "I32": CLT_I32,
    "I64": CLT_I64,
    "Key": CLT_Key,
    "PublicKey": CLT_PublicKey,
    "Result": CLT_Result,
    "String": CLT_String,
    "U8": CLT_U8,
    "U32": CLT_U32,
    "U64": CLT_U64,
    "U128": CLT_U128,
    "U256": CLT_U256,
    "U512": CLT_U512,
    "Unit": CLT_Unit,
    "URef": CLT_URef,
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
        return CLT_List(
            decode(encoded["List"])
        )

    elif "Map" in encoded:
        return CLT_Map(
            decode(encoded["Map"]["key"]),
            decode(encoded["Map"]["value"])
            )

    elif "Option" in encoded:
        return CLT_Option(
            decode(encoded["Option"])
        )

    elif "Tuple1" in encoded:
        return CLT_Tuple1(
            decode(encoded["Tuple1"])
        )

    elif "Tuple2" in encoded:
        return CLT_Tuple2(
            decode(encoded["Tuple2"][0]),
            decode(encoded["Tuple2"][1])
        )

    elif "Tuple3" in encoded:
        return CLT_Tuple3(
            decode(encoded["Tuple3"][0]),
            decode(encoded["Tuple3"][1]),
            decode(encoded["Tuple3"][2])
            )

    else:
        raise ValueError("Invalid CL type JSON representation")
