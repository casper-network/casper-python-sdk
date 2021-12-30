import typing

from pycspr.types import cl_types
from pycspr.types import CL_TypeKey


def encode(entity: cl_types.CL_Type) -> typing.Union[str, dict]:
    """Encodes a CL type as a JSON compatible string or dictionary.

    :param entity: A CL type to be encoded.
    :returns: A JSON compatible string or dictionary.
    
    """
    try:
        encoder = _ENCODERS_COMPLEX[entity.type_key]
    except KeyError:
        try:
            return _ENCODERS_SIMPLE[entity.type_key]
        except KeyError:
            raise ValueError("Invalid CL type")
    else:
        return encoder(entity)


def _encode_byte_array(entity: cl_types.CL_Type_ByteArray):
    return {
        "ByteArray": entity.size
    }


def _encode_list(entity: cl_types.CL_Type_List):
    return {
        "List": encode(entity.inner_type)
    }


def _encode_map(entity: cl_types.CL_Type_Map):
    return {
        "Map": {
            "key": encode(entity.key_type),
            "value": encode(entity.value_type)
        }
    }


def _encode_option(entity: cl_types.CL_Type_Option):
    return {
        "Option": encode(entity.inner_type)
    }


def _encode_tuple_1(entity: cl_types.CL_Type_Tuple1):
    return {
        "Tuple1": encode(entity.t0_type)
    }


def _encode_tuple_2(entity: cl_types.CL_Type_Tuple1):
    return {
        "Tuple2": [
            encode(entity.t0_type),
            encode(entity.t1_type),
        ]
    }


def _encode_tuple_3(entity: cl_types.CL_Type_Tuple1):
    return {
        "Tuple3": [
            encode(entity.t0_type),
            encode(entity.t1_type),
            encode(entity.t2_type)
        ]
    }


_ENCODERS_COMPLEX: dict = {
    CL_TypeKey.BYTE_ARRAY: _encode_byte_array,
    CL_TypeKey.LIST: _encode_list,
    CL_TypeKey.MAP: _encode_map,
    CL_TypeKey.OPTION: _encode_option,
    CL_TypeKey.TUPLE_1: _encode_tuple_1,
    CL_TypeKey.TUPLE_2: _encode_tuple_2,
    CL_TypeKey.TUPLE_3: _encode_tuple_3,
}

_ENCODERS_SIMPLE: dict = {
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
