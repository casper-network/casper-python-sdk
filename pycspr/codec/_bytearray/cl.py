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
from pycspr.types.cl import CLType


_ENCODERS = {
    CLType.ANY: cl_any,
    CLType.BOOL: cl_boolean,
    CLType.BYTE_ARRAY: cl_byte_array,
    CLType.I32: cl_i32,
    CLType.I64: cl_i64,
    CLType.KEY: cl_key,
    CLType.LIST: cl_list,
    CLType.MAP: cl_map,
    CLType.OPTION: cl_option,
    CLType.PUBLIC_KEY: cl_public_key,
    CLType.RESULT: cl_result,
    CLType.STRING: cl_string,
    CLType.TUPLE_1: cl_tuple1,
    CLType.TUPLE_2: cl_tuple2,
    CLType.TUPLE_3: cl_tuple3,
    CLType.U8: cl_u8,
    CLType.U32: cl_u32,
    CLType.U64: cl_u64,
    CLType.U128: cl_u128,
    CLType.U256: cl_u256,
    CLType.U512: cl_u512,
    CLType.UNIT: cl_unit,
    CLType.UREF: cl_uref,
}


def to_bytes(typeof: CLType, value: object) -> bytearray:
    return [typeof.value] + _ENCODERS[typeof](value)
