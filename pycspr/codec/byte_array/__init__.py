import typing

from pycspr.codec.byte_array import cl_boolean
from pycspr.codec.byte_array import cl_bytearray
from pycspr.codec.byte_array import cl_i32
from pycspr.codec.byte_array import cl_i64
from pycspr.codec.byte_array import cl_key
from pycspr.codec.byte_array import cl_option
from pycspr.codec.byte_array import cl_public_key
from pycspr.codec.byte_array import cl_string
from pycspr.codec.byte_array import cl_u8
from pycspr.codec.byte_array import cl_u32
from pycspr.codec.byte_array import cl_u64
from pycspr.codec.byte_array import cl_u128
from pycspr.codec.byte_array import cl_u256
from pycspr.codec.byte_array import cl_u512
from pycspr.codec.byte_array import cl_unit
from pycspr.codec.byte_array import cl_uref
from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLValue


# LIST = 14
# RESULT = 16
# MAP = 17
# TUPLE_1 = 18
# TUPLE_2 = 19
# TUPLE_3 = 20
# ANY = 21


# Map: entity type <-> codec.
_CODECS = {
    CLTypeKey.BOOL: cl_boolean,
    CLTypeKey.BYTE_ARRAY: cl_bytearray,
    CLTypeKey.I32: cl_i32,
    CLTypeKey.I64: cl_i64,
    CLTypeKey.KEY: cl_key,
    CLTypeKey.OPTION: cl_option,    
    CLTypeKey.PUBLIC_KEY: cl_public_key,
    CLTypeKey.STRING: cl_string,
    CLTypeKey.U8: cl_u8,
    CLTypeKey.U32: cl_u32,
    CLTypeKey.U64: cl_u64,
    CLTypeKey.U128: cl_u128,    
    CLTypeKey.U256: cl_u256,    
    CLTypeKey.U512: cl_u512,
    CLTypeKey.UNIT: cl_unit,
    CLTypeKey.UREF: cl_uref,
}


def encode(value: CLValue):
    """Encodes a value as an array of bytes decodeable by a CSPR agent.
    
    """
    codec = _CODECS[value.cl_type.typeof]
    if type(value.cl_type) == CLType_Option:
        return codec.encode(value)
    else:
        return codec.encode(value.parsed)
