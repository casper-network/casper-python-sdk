from pycspr.codec._bytearray import cl_u32
from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType_ByteArray
from pycspr.types.cl import CLType_List
from pycspr.types.cl import CLType_Map
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLType_Tuple1
from pycspr.types.cl import CLType_Tuple2
from pycspr.types.cl import CLType_Tuple3



def _encode_any(instance: object) ->  bytearray:
    raise NotImplementedError()


def _encode_byte_array(instance: CLType_ByteArray) ->  bytearray:
    return cl_u32.encode(instance.size)


def _encode_list(instance: CLType_List) ->  bytearray:
    return encode(instance.typeof_inner)


def _encode_map(instance: CLType_Map) ->  bytearray:
    return encode(instance.typeof_key) + \
           encode(instance.typeof_value)


def _encode_option(instance: CLType_Option) ->  bytearray:
    return encode(instance.typeof_inner)


def _encode_result(instance: object) -> bytearray:
    raise NotImplementedError()


def _encode_simple(instance: CLType) ->  bytearray:
    return []


def _encode_tuple_1(instance: CLType_Tuple1) ->  bytearray:
    return encode(instance.typeof_t0)


def _encode_tuple_2(instance: CLType_Tuple2) ->  bytearray:
    return encode(instance.typeof_t0) + \
           encode(instance.typeof_t1)


def _encode_tuple_3(instance: CLType_Tuple3) -> bytearray:
    return encode(instance.typeof_t0) + \
           encode(instance.typeof_t1) + \
           encode(instance.typeof_t2)


# Map: cl type enum <-> encoding function.
_ENCODERS = {
    CLTypeKey.BOOL: _encode_simple,
    CLTypeKey.I32: _encode_simple,
    CLTypeKey.I64: _encode_simple,
    CLTypeKey.U8: _encode_simple,
    CLTypeKey.U3: _encode_simple,
    CLTypeKey.U64: _encode_simple,
    CLTypeKey.U128: _encode_simple,
    CLTypeKey.U256: _encode_simple,
    CLTypeKey.U512: _encode_simple,
    CLTypeKey.UNIT: _encode_simple,
    CLTypeKey.STRING: _encode_simple,
    CLTypeKey.KEY: _encode_simple,
    CLTypeKey.UREF: _encode_simple,
    CLTypeKey.OPTION: _encode_option,
    CLTypeKey.LIST: _encode_list,
    CLTypeKey.BYTE_ARRAY: _encode_byte_array,
    CLTypeKey.RESULT: _encode_result,
    CLTypeKey.MAP: _encode_map,
    CLTypeKey.TUPLE_1: _encode_tuple_1,
    CLTypeKey.TUPLE_2: _encode_tuple_2,
    CLTypeKey.TUPLE_3: _encode_tuple_3,
    CLTypeKey.ANY: _encode_any,
    CLTypeKey.PUBLIC_KEY: _encode_simple,
}


def to_bytes(instance: CLType) -> bytearray:
    """Maps cl type information to a bytearray for interpretation by a CSPR node.
    
    :param CLType instance: Type information related to a value interpretable by a CSPR node.

    """
    return [instance.typeof.value] + _ENCODERS[instance.typeof](instance)
