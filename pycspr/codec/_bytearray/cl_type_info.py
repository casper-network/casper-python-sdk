from pycspr.codec._bytearray import cl_u32
from pycspr.types.cl import CLType
from pycspr.types.cl import CLTypeInfo
from pycspr.types.cl import CLTypeInfoForByteArray
from pycspr.types.cl import CLTypeInfoForList
from pycspr.types.cl import CLTypeInfoForMap
from pycspr.types.cl import CLTypeInfoForOption
from pycspr.types.cl import CLTypeInfoForTuple1
from pycspr.types.cl import CLTypeInfoForTuple2
from pycspr.types.cl import CLTypeInfoForTuple3



def _encode_any(instance: object) ->  bytearray:
    raise NotImplementedError()


def _encode_byte_array(instance: CLTypeInfoForByteArray) ->  bytearray:
    return cl_u32.encode(instance.size)


def _encode_list(instance: CLTypeInfoForList) ->  bytearray:
    return encode(instance.typeof_inner)


def _encode_map(instance: CLTypeInfoForMap) ->  bytearray:
    return encode(instance.typeof_key) + \
           encode(instance.typeof_value)


def _encode_option(instance: CLTypeInfoForOption) ->  bytearray:
    return encode(instance.typeof_inner)


def _encode_result(instance: object) -> bytearray:
    raise NotImplementedError()


def _encode_simple(instance: CLTypeInfo) ->  bytearray:
    return []


def _encode_tuple_1(instance: CLTypeInfoForTuple1) ->  bytearray:
    return encode(instance.typeof_t0)


def _encode_tuple_2(instance: CLTypeInfoForTuple2) ->  bytearray:
    return encode(instance.typeof_t0) + \
           encode(instance.typeof_t1)


def _encode_tuple_3(instance: CLTypeInfoForTuple3) -> bytearray:
    return encode(instance.typeof_t0) + \
           encode(instance.typeof_t1) + \
           encode(instance.typeof_t2)


# Map: cl type enum <-> encoding function.
_ENCODERS = {
    CLType.BOOL: _encode_simple,
    CLType.I32: _encode_simple,
    CLType.I64: _encode_simple,
    CLType.U8: _encode_simple,
    CLType.U3: _encode_simple,
    CLType.U64: _encode_simple,
    CLType.U128: _encode_simple,
    CLType.U256: _encode_simple,
    CLType.U512: _encode_simple,
    CLType.UNIT: _encode_simple,
    CLType.STRING: _encode_simple,
    CLType.KEY: _encode_simple,
    CLType.UREF: _encode_simple,
    CLType.OPTION: _encode_option,
    CLType.LIST: _encode_list,
    CLType.BYTE_ARRAY: _encode_byte_array,
    CLType.RESULT: _encode_result,
    CLType.MAP: _encode_map,
    CLType.TUPLE_1: _encode_tuple_1,
    CLType.TUPLE_2: _encode_tuple_2,
    CLType.TUPLE_3: _encode_tuple_3,
    CLType.ANY: _encode_any,
    CLType.PUBLIC_KEY: _encode_simple,
}


def to_bytes(instance: CLTypeInfo) -> bytearray:
    """Maps cl type information to a bytearray for interpretation by a CSPR node.
    
    :param CLTypeInfo instance: Type information related to a value interpretable by a CSPR node.

    """
    return [instance.typeof.value] + _ENCODERS[instance.typeof](instance)
