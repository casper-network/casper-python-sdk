import typing

from pycspr.types.cl.types import CL_Type
from pycspr.types.cl.types import CL_TypeKey
from pycspr.types.cl.types import CL_Type_ByteArray
from pycspr.types.cl.types import CL_Type_List
from pycspr.types.cl.types import CL_Type_Map
from pycspr.types.cl.types import CL_Type_Option
from pycspr.types.cl.types import CL_Type_Tuple1


def encode(entity: CL_Type) -> typing.Union[str, dict]:
    """Encoder: CL type -> JSON blob.

    :param entity: A CL type to be encoded.
    :returns: A JSON compatible string or dictionary.

    """
    if entity.type_key in _ENCODERS["complex"]:
        return _ENCODERS["complex"][entity.type_key](entity)
    elif entity.type_key in _ENCODERS["simple"]:
        return _ENCODERS["simple"][entity.type_key]
    else:
        raise ValueError("Invalid CL type")


def _encode_byte_array(entity: CL_Type_ByteArray):
    return {
        "ByteArray": entity.size
    }


def _encode_list(entity: CL_Type_List):
    return {
        "List": encode(entity.inner_type)
    }


def _encode_map(entity: CL_Type_Map):
    return {
        "Map": {
            "key": encode(entity.key_type),
            "value": encode(entity.value_type)
        }
    }


def _encode_option(entity: CL_Type_Option):
    return {
        "Option": encode(entity.inner_type)
    }


def _encode_tuple_1(entity: CL_Type_Tuple1):
    return {
        "Tuple1": encode(entity.t0_type)
    }


def _encode_tuple_2(entity: CL_Type_Tuple1):
    return {
        "Tuple2": [
            encode(entity.t0_type),
            encode(entity.t1_type),
        ]
    }


def _encode_tuple_3(entity: CL_Type_Tuple1):
    return {
        "Tuple3": [
            encode(entity.t0_type),
            encode(entity.t1_type),
            encode(entity.t2_type)
        ]
    }


_ENCODERS: dict = {
    "complex": {
        CL_TypeKey.BYTE_ARRAY: _encode_byte_array,
        CL_TypeKey.LIST: _encode_list,
        CL_TypeKey.MAP: _encode_map,
        CL_TypeKey.OPTION: _encode_option,
        CL_TypeKey.TUPLE_1: _encode_tuple_1,
        CL_TypeKey.TUPLE_2: _encode_tuple_2,
        CL_TypeKey.TUPLE_3: _encode_tuple_3,
    },
    "simple": {
        CL_TypeKey.ANY: "Any",
        CL_TypeKey.BOOL: "Bool",
        CL_TypeKey.I32: "I32",
        CL_TypeKey.I64: "I64",
        CL_TypeKey.KEY: "Key",
        CL_TypeKey.PUBLIC_KEY: "PublicKey",
        CL_TypeKey.RESULT: "Result",
        CL_TypeKey.STRING: "String",
        CL_TypeKey.U8: "U8",
        CL_TypeKey.U32: "U32",
        CL_TypeKey.U64: "U64",
        CL_TypeKey.U128: "U128",
        CL_TypeKey.U256: "U256",
        CL_TypeKey.U512: "U512",
        CL_TypeKey.UNIT: "Unit",
        CL_TypeKey.UREF: "URef",        
    }
}
