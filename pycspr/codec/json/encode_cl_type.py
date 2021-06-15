from pycspr.types.cl import CLType
from pycspr.types.cl import CLType_ByteArray
from pycspr.types.cl import CLType_List
from pycspr.types.cl import CLType_Map
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLType_Simple
from pycspr.types.cl import CLType_Tuple1
from pycspr.types.cl import CLType_Tuple2
from pycspr.types.cl import CLType_Tuple3



# Map: domain type <-> encoder.
_ENCODERS = {
    # Byte array.
    CLType_ByteArray: lambda e: {
        "ByteArray": e.size
    },

    # List.
    CLType_List: lambda e: {
        "List": encode(e.inner_type)
    },

    # Map.
    CLType_Map: lambda e: {
        "Map": encode(e.inner_type)
    },

    # Optional.
    CLType_Option: lambda e: {
        "Option": encode(e.inner_type)
    },

    # Simple type.
    CLType_Simple: lambda e: e.typeof.name,

    # 1-ary tuple.
    CLType_Tuple1: lambda e: {
        "Tuple1": encode(e.t0_type)
    },

    # 2-ary tuple.
    CLType_Tuple2: lambda e: {
        "Tuple2": [encode(e.t0_type), encode(e.t1_type)]
    },

    # 3-ary tuple.
    CLType_Tuple3: lambda e: {
        "Tuple3": [encode(e.t0_type), encode(e.t1_type), encode(e.t2_type)]
    },
}


def encode(entity: CLType):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return _ENCODERS[type(entity)](entity)
