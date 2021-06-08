from pycspr.codec._bytearray import cl_any
from pycspr.codec._bytearray import cl_boolean
from pycspr.codec._bytearray import cl_byte_array
from pycspr.codec._bytearray import cl_i32
from pycspr.codec._bytearray import cl_i64
from pycspr.codec._bytearray import cl_key
from pycspr.codec._bytearray import cl_list
from pycspr.codec._bytearray import cl_map
from pycspr.codec._bytearray import cl_option
from pycspr.codec._bytearray import cl_public_key
from pycspr.codec._bytearray import cl_result
from pycspr.codec._bytearray import cl_string
from pycspr.codec._bytearray import cl_tuple1
from pycspr.codec._bytearray import cl_tuple2
from pycspr.codec._bytearray import cl_tuple3
from pycspr.codec._bytearray import cl_u8
from pycspr.codec._bytearray import cl_u32
from pycspr.codec._bytearray import cl_u64
from pycspr.codec._bytearray import cl_u128
from pycspr.codec._bytearray import cl_u256
from pycspr.codec._bytearray import cl_u512
from pycspr.codec._bytearray import cl_unit
from pycspr.codec._bytearray import cl_uref
from pycspr.types.cl import CLTypeKey


_ENCODERS = {
    CLTypeKey.ANY: cl_any,
    CLTypeKey.BOOL: cl_boolean,
    CLTypeKey.BYTE_ARRAY: cl_byte_array,
    CLTypeKey.I32: cl_i32,
    CLTypeKey.I64: cl_i64,
    CLTypeKey.KEY: cl_key,
    CLTypeKey.LIST: cl_list,
    CLTypeKey.MAP: cl_map,
    CLTypeKey.OPTION: cl_option,
    CLTypeKey.PUBLIC_KEY: cl_public_key,
    CLTypeKey.RESULT: cl_result,
    CLTypeKey.STRING: cl_string,
    CLTypeKey.TUPLE_1: cl_tuple1,
    CLTypeKey.TUPLE_2: cl_tuple2,
    CLTypeKey.TUPLE_3: cl_tuple3,
    CLTypeKey.U8: cl_u8,
    CLTypeKey.U32: cl_u32,
    CLTypeKey.U64: cl_u64,
    CLTypeKey.U128: cl_u128,
    CLTypeKey.U256: cl_u256,
    CLTypeKey.U512: cl_u512,
    CLTypeKey.UNIT: cl_unit,
    CLTypeKey.UREF: cl_uref,
}


def to_bytes(typeof: CLTypeKey, value: object) -> bytearray:
    return [typeof.value] + _ENCODERS[typeof](value)
