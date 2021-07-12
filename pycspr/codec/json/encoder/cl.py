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
        "parsed": str(entity.parsed),
    }
