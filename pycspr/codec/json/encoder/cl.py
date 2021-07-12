from pycspr.codec.byte_array import encode as byte_array_encoder
from pycspr.types import CLValue
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
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
        CLType_Simple: lambda: entity.typeof.name,

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
            "Tuple3": [encode_cl_type(entity.t0_type), encode_cl_type(entity.t1_type), encode_cl_type(entity.t2_type)]
        },
    }

    return _ENCODERS[type(entity)]()


def encode_cl_value(entity: CLValue) -> dict:
    """Encodes a CL value.

    """
    return {
        "bytes": bytes(byte_array_encoder(entity)).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": encode_cl_value_parsed(entity.cl_type, entity.parsed),
    }


def encode_cl_value_parsed(type_info: CLType, parsed: object) -> str:
    """Encodes a CL value.

    """

    if type_info.typeof in TYPES_NUMERIC:
        return str(int(parsed))
    elif type_info.typeof == CLTypeKey.BYTE_ARRAY:
        return parsed
    elif type_info.typeof == CLTypeKey.OPTION:
        print(1234, parsed)
        return parsed
    else:
        return str(parsed)
    


    # CLTypeKey.ANY: encode_any,
    # CLTypeKey.BOOL: encode_bool,
    # CLTypeKey.BYTE_ARRAY: encode_byte_array,
    # CLTypeKey.I32: encode_i32,
    # CLTypeKey.I64: encode_i64,
    # CLTypeKey.KEY: encode_key,
    # CLTypeKey.LIST: encode_list,    
    # CLTypeKey.MAP: encode_map,    
    # CLTypeKey.OPTION: encode_option,    
    # CLTypeKey.PUBLIC_KEY: encode_public_key,
    # CLTypeKey.STRING: encode_string,
    # CLTypeKey.TUPLE_1: encode_tuple1,
    # CLTypeKey.TUPLE_2: encode_tuple2,
    # CLTypeKey.TUPLE_3: encode_tuple3,
    # CLTypeKey.U8: encode_u8,
    # CLTypeKey.U32: encode_u32,
    # CLTypeKey.U64: encode_u64,
    # CLTypeKey.U128: encode_u128,    
    # CLTypeKey.U256: encode_u256,
    # CLTypeKey.U512: encode_u512,
    # CLTypeKey.UNIT: encode_unit,
    # CLTypeKey.RESULT: encode_result,
    # CLTypeKey.UREF: encode_uref,
