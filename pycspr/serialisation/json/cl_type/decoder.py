import typing

from pycspr.types.cl.types import CL_Type
from pycspr.types.cl.types import CL_Type_Any
from pycspr.types.cl.types import CL_Type_Bool
from pycspr.types.cl.types import CL_Type_ByteArray
from pycspr.types.cl.types import CL_Type_I32
from pycspr.types.cl.types import CL_Type_I64
from pycspr.types.cl.types import CL_Type_U8
from pycspr.types.cl.types import CL_Type_U32
from pycspr.types.cl.types import CL_Type_U64
from pycspr.types.cl.types import CL_Type_U128
from pycspr.types.cl.types import CL_Type_U256
from pycspr.types.cl.types import CL_Type_U512
from pycspr.types.cl.types import CL_Type_Key
from pycspr.types.cl.types import CL_Type_List
from pycspr.types.cl.types import CL_Type_Map
from pycspr.types.cl.types import CL_Type_Option
from pycspr.types.cl.types import CL_Type_PublicKey
from pycspr.types.cl.types import CL_Type_Result
from pycspr.types.cl.types import CL_Type_String
from pycspr.types.cl.types import CL_Type_Tuple1
from pycspr.types.cl.types import CL_Type_Tuple2
from pycspr.types.cl.types import CL_Type_Tuple3
from pycspr.types.cl.types import CL_Type_Unit
from pycspr.types.cl.types import CL_Type_URef


def decode(encoded: typing.Union[str, dict]) -> CL_Type:
    """Decoder: CL type info <- JSON blob.

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
    return CL_Type_ByteArray(obj["ByteArray"])


def _decode_list(obj: dict):
    return CL_Type_List(decode(obj["List"]))


def _decode_map(obj: dict):
    return CL_Type_Map(
        decode(obj["Map"]["key"]),
        decode(obj["Map"]["value"])
        )


def _decode_option(obj: dict):
    return CL_Type_Option(decode(obj["Option"]))


def _decode_tuple_1(obj: dict):
    return CL_Type_Tuple1(decode(obj["Tuple1"]))


def _decode_tuple_2(obj: dict):
    return CL_Type_Tuple2(
        decode(obj["Tuple2"][0]),
        decode(obj["Tuple2"][1])
        )


def _decode_tuple_3(obj: dict):
    return CL_Type_Tuple3(
        decode(obj["Tuple3"][0]),
        decode(obj["Tuple3"][1]),
        decode(obj["Tuple3"][2])
        )


_SIMPLE_TYPES = {
    "Any": CL_Type_Any,
    "Bool": CL_Type_Bool,
    "I32": CL_Type_I32,
    "I64": CL_Type_I64,
    "Key": CL_Type_Key,
    "PublicKey": CL_Type_PublicKey,
    "Result": CL_Type_Result,
    "String": CL_Type_String,
    "U8": CL_Type_U8,
    "U32": CL_Type_U32,
    "U64": CL_Type_U64,
    "U128": CL_Type_U128,
    "U256": CL_Type_U256,
    "U512": CL_Type_U512,
    "Unit": CL_Type_Unit,
    "URef": CL_Type_URef,
}
