import typing

from pycspr.codec.byte_array import cl
from pycspr.codec.byte_array import deploy
from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLValue


# Map: entity type <-> codec.
_CODECS = {
    CLTypeKey.ANY: None,
    CLTypeKey.BOOL: cl.encode_bool,
    CLTypeKey.BYTE_ARRAY: cl.encode_byte_array,
    CLTypeKey.I32: cl.encode_i32,
    CLTypeKey.I64: cl.encode_i64,
    CLTypeKey.KEY: cl.encode_key,
    CLTypeKey.LIST: cl.encode_list,    
    CLTypeKey.MAP: cl.encode_map,    
    CLTypeKey.OPTION: cl.encode_option,    
    CLTypeKey.PUBLIC_KEY: cl.encode_public_key,
    CLTypeKey.STRING: cl.encode_string,
    CLTypeKey.TUPLE_1: cl.encode_tuple1,
    CLTypeKey.TUPLE_2: cl.encode_tuple2,
    CLTypeKey.TUPLE_3: cl.encode_tuple3,
    CLTypeKey.U8: cl.encode_u8,
    CLTypeKey.U32: cl.encode_u32,
    CLTypeKey.U64: cl.encode_u64,
    CLTypeKey.U128: cl.encode_u128,    
    CLTypeKey.U256: cl.encode_u256,
    CLTypeKey.U512: cl.encode_u512,
    CLTypeKey.UNIT: cl.encode_unit,
    CLTypeKey.RESULT: None,
    CLTypeKey.UREF: cl.encode_uref,
}


def encode(value: CLValue) -> typing.List[int]:
    """Encodes a value as an array of bytes decodeable by a CSPR agent.
    
    """
    codec = _CODECS[value.cl_type.typeof]
    if type(value.cl_type) == CLType_Option:
        return codec.encode(value)
    else:
        return codec.encode(value.parsed)
