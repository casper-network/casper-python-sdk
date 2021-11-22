from pycspr import serialisation
from pycspr.types import CLValue
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_Key
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLTypeKey
from pycspr.types import TYPES_NUMERIC
from pycspr.types import StateKeyType


def encode_cl_type(entity: CLType) -> dict:
    """Encodes a CL type.

    """
    _ENCODERS = {
        # Byte array.
        CLType_ByteArray: lambda: {
            "ByteArray": entity.size
        },

        # List.
        CLType_List: lambda: {
            "List": encode_cl_type(entity.inner_type)
        },

        # Map.
        CLType_Map: lambda: {
            "Map": encode_cl_type(entity.inner_type)
        },

        # Optional.
        CLType_Option: lambda: {
            "Option": encode_cl_type(entity.inner_type)
        },

        # Simple type.
        CLType_Simple: lambda: encode_cl_type_key(entity.type_key),

        # Storage Key.
        CLType_Key: lambda: "Key",

        # 1-ary tuple.
        CLType_Tuple1: lambda: {
            "Tuple1": encode_cl_type(entity.t0_type)
        },

        # 2-ary tuple.
        CLType_Tuple2: lambda: {
            "Tuple2": [encode_cl_type(entity.t0_type), encode_cl_type(entity.t1_type)]
        },

        # 3-ary tuple.
        CLType_Tuple3: lambda: {
            "Tuple3": [
                encode_cl_type(entity.t0_type),
                encode_cl_type(entity.t1_type),
                encode_cl_type(entity.t2_type)
                ]
        },
    }

    return _ENCODERS[type(entity)]()


# Map: CL type key <-> JSON type tag.
_CL_TYPE_KEY_JSON_TAG = {
    CLTypeKey.BOOL: "Bool",
    CLTypeKey.KEY: "Key",
    CLTypeKey.PUBLIC_KEY: "PublicKey",
    CLTypeKey.STRING: "String",
    CLTypeKey.UNIT: "Unit",
    CLTypeKey.UREF: "URef",
}


def encode_cl_type_key(type_key: CLTypeKey) -> str:
    """Encodes a CL type key.

    """
    try:
        return _CL_TYPE_KEY_JSON_TAG[type_key]
    except KeyError:
        return type_key.name


def encode_cl_value(entity: CLValue) -> dict:
    """Encodes a CL value.

    """
    return {
        "bytes": serialisation.to_bytes(entity).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": _encode_cl_value_parsed(entity, entity.cl_type),
    }


def _encode_cl_value_parsed(entity: CLValue, type_info: CLType) -> str:
    """Encodes parsed represenation of a CL value.  This is uninterpreted by a node but useful nonetheless.

    """
    if type_info.type_key in TYPES_NUMERIC:
        return str(int(entity.parsed))
    elif type_info.type_key == CLTypeKey.BYTE_ARRAY:
        return entity.parsed.hex()
    elif type_info.type_key == CLTypeKey.KEY:
        if type_info.key_type == StateKeyType.ACCOUNT:
            return {
                "Account": entity.parsed.as_string()
            }
        return entity.parsed.as_string()
    elif type_info.type_key == CLTypeKey.PUBLIC_KEY:
        return entity.parsed.account_key.hex()
    elif type_info.type_key == CLTypeKey.UREF:
        return entity.parsed.as_string()
    elif type_info.type_key == CLTypeKey.OPTION:
        return _encode_cl_value_parsed(entity, type_info.inner_type)
    else:
        return str(entity.parsed)
