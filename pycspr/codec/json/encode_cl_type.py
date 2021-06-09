from pycspr.types.cl import CLType
from pycspr.types.cl import CLType_ByteArray
from pycspr.types.cl import CLType_List
from pycspr.types.cl import CLType_Map
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLType_Simple
from pycspr.types.cl import CLType_Tuple1
from pycspr.types.cl import CLType_Tuple2
from pycspr.types.cl import CLType_Tuple3



def _encode_byte_array(entity: CLType_ByteArray) -> dict:
    return {
        "ByteArray": entity.size
    }


def _encode_list(entity: CLType_List) -> dict:
    return {
        "List": encode(entity.inner_type_info)
    }


def _encode_map(entity: CLType_Map) -> dict:
    return {
        "Map": encode(entity.inner_type_info)
    }


def _encode_option(entity: CLType_Option) -> dict:
    return {
        "Option": encode(entity.inner_type_info)
    }


def _encode_simple(entity: CLType_Simple) -> str:
    return entity.typeof.name


def _encode_tuple_1(entity: CLType_Tuple1) -> dict:
    return {
        "Tuple1": encode(entity.t0_type_info)
    }


def _encode_tuple_2(entity: CLType_Tuple2) -> dict:
    return {
        "Tuple2": [encode(entity.t0_type_info), encode(entity.t1_type_info)]
    }


def _encode_tuple_3(entity: CLType_Tuple3) -> dict:
    return {
        "Tuple3": [encode(entity.t0_type_info), encode(entity.t1_type_info), encode(entity.t2_type_info)]
    }


# Map: domain type <-> encoder.
_ENCODERS = {
    CLType_ByteArray: _encode_byte_array,
    CLType_List: _encode_list,
    CLType_Map: _encode_map,
    CLType_Option: _encode_option,
    CLType_Simple: _encode_simple,
    CLType_Tuple1: _encode_tuple_1,
    CLType_Tuple2: _encode_tuple_2,
    CLType_Tuple3: _encode_tuple_3,
}


def encode(entity: CLType):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return _ENCODERS[type(entity)](entity)
