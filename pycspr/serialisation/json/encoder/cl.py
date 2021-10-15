from pycspr import serialisation
from pycspr.types import CLValue
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_StorageKey
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLTypeKey
from pycspr.types import TYPES_NUMERIC


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
        CLType_StorageKey: "Key",

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


def encode_cl_type_key(entity: CLTypeKey) -> str:
    """Encodes a CL type key.

    """
    if entity == CLTypeKey.BOOL:
        return "Bool"
    elif entity == CLTypeKey.UNIT:
        return "Unit"
    elif entity == CLTypeKey.STRING:
        return "String"
    elif entity == CLTypeKey.KEY:
        return "Key"
    elif entity == CLTypeKey.UREF:
        return "URef"
    elif entity == CLTypeKey.PUBLIC_KEY:
        return "PublicKey"
    else:
        return entity.name


def encode_cl_type_storage_key(entity: CLTypeKey) -> str:
    """Encodes a CL type key.

    """
    if entity == CLTypeKey.BOOL:
        return "Bool"
    elif entity == CLTypeKey.UNIT:
        return "Unit"
    elif entity == CLTypeKey.STRING:
        return "String"
    elif entity == CLTypeKey.KEY:
        return "Key"
    elif entity == CLTypeKey.UREF:
        return "URef"
    elif entity == CLTypeKey.PUBLIC_KEY:
        return "PublicKey"
    else:
        return entity.name


def encode_cl_value(entity: CLValue) -> dict:
    """Encodes a CL value.

    """
    def _encode_parsed(type_info: CLType) -> str:
        if type_info.type_key in TYPES_NUMERIC:
            return str(int(entity.parsed))
        elif type_info.type_key == CLTypeKey.BYTE_ARRAY:
            return entity.parsed.hex()
        elif type_info.type_key == CLTypeKey.KEY:
            return entity.parsed.as_string()
        elif type_info.type_key == CLTypeKey.PUBLIC_KEY:
            return entity.parsed.account_key.hex()
        elif type_info.type_key == CLTypeKey.UREF:
            return entity.parsed.as_string()
        elif type_info.type_key == CLTypeKey.OPTION:
            return _encode_parsed(type_info.inner_type)
        else:
            return str(entity.parsed)

    return {
        "bytes": serialisation.to_bytes(entity).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": _encode_parsed(entity.cl_type),
    }
