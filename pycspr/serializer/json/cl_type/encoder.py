import typing

from pycspr.types.cl.types import CLT_Type
from pycspr.types.cl.types import CLT_TypeKey
from pycspr.types.cl.types import CLT_Type_ByteArray
from pycspr.types.cl.types import CLT_Type_List
from pycspr.types.cl.types import CLT_Type_Map
from pycspr.types.cl.types import CLT_Type_Option
from pycspr.types.cl.types import CLT_Type_Tuple1


def encode(entity: CLT_Type) -> typing.Union[str, dict]:
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


def _encode_byte_array(entity: CLT_Type_ByteArray):
    return {
        "ByteArray": entity.size
    }


def _encode_list(entity: CLT_Type_List):
    return {
        "List": encode(entity.inner_type)
    }


def _encode_map(entity: CLT_Type_Map):
    return {
        "Map": {
            "key": encode(entity.key_type),
            "value": encode(entity.value_type)
        }
    }


def _encode_option(entity: CLT_Type_Option):
    return {
        "Option": encode(entity.inner_type)
    }


def _encode_tuple_1(entity: CLT_Type_Tuple1):
    return {
        "Tuple1": encode(entity.t0_type)
    }


def _encode_tuple_2(entity: CLT_Type_Tuple1):
    return {
        "Tuple2": [
            encode(entity.t0_type),
            encode(entity.t1_type),
        ]
    }


def _encode_tuple_3(entity: CLT_Type_Tuple1):
    return {
        "Tuple3": [
            encode(entity.t0_type),
            encode(entity.t1_type),
            encode(entity.t2_type)
        ]
    }


_ENCODERS: dict = {
    "complex": {
        CLT_TypeKey.BYTE_ARRAY: _encode_byte_array,
        CLT_TypeKey.LIST: _encode_list,
        CLT_TypeKey.MAP: _encode_map,
        CLT_TypeKey.OPTION: _encode_option,
        CLT_TypeKey.TUPLE_1: _encode_tuple_1,
        CLT_TypeKey.TUPLE_2: _encode_tuple_2,
        CLT_TypeKey.TUPLE_3: _encode_tuple_3,
    },
    "simple": {
        CLT_TypeKey.ANY: "Any",
        CLT_TypeKey.BOOL: "Bool",
        CLT_TypeKey.I32: "I32",
        CLT_TypeKey.I64: "I64",
        CLT_TypeKey.KEY: "Key",
        CLT_TypeKey.PUBLIC_KEY: "PublicKey",
        CLT_TypeKey.RESULT: "Result",
        CLT_TypeKey.STRING: "String",
        CLT_TypeKey.U8: "U8",
        CLT_TypeKey.U32: "U32",
        CLT_TypeKey.U64: "U64",
        CLT_TypeKey.U128: "U128",
        CLT_TypeKey.U256: "U256",
        CLT_TypeKey.U512: "U512",
        CLT_TypeKey.UNIT: "Unit",
        CLT_TypeKey.UREF: "URef",
    }
}
