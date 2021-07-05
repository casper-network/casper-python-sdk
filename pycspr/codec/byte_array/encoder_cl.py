import typing

from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import int_to_le_bytes_trimmed
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType_ByteArray
from pycspr.types.cl import CLType_List
from pycspr.types.cl import CLType_Map
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLType_Simple
from pycspr.types.cl import CLType_Tuple1
from pycspr.types.cl import CLType_Tuple2
from pycspr.types.cl import CLType_Tuple3
from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLValue
from pycspr.types.deploy import PublicKey
from pycspr.utils.constants import NUMERIC_CONSTRAINTS



def encode_any(value: object):
    """Encodes a domain value: a value under CL storage with an unassigned type.
    
    """
    raise NotImplementedError()


def encode_bool(value: bool):
    """Encodes a domain value: bool.
    
    """
    return [int(value)]


def encode_byte_array(value: typing.Union[bytes, str]):    
    """Encodes a domain value: byte array.
    
    """
    if isinstance(value, bytes):
        return [int(i) for i in value]
    elif isinstance(value, list):
        return value
    else:
        return [int(i) for i in bytes.fromhex(value)]


def encode_cl_value(entity: CLValue) -> typing.List[int]:
    """Encodes a domain value: CL value.
    
    """
    return encode_u8_array(encode(entity)) + encode_cl_type(entity.cl_type)


def encode_cl_type(entity: CLType) -> typing.List[int]:
    """Encodes a domain value: CL type.
    
    """
    def _encode_byte_array():
        return [entity.typeof.value] + encode_u32(entity.size)

    def _encode_list():
        raise NotImplementedError()

    def _encode_map():
        raise NotImplementedError()

    def _encode_option():
        return [entity.typeof.value] + encode_cl_type(entity.inner_type)

    def _encode_simple():
        return [entity.typeof.value]

    def _encode_tuple_1():
        raise NotImplementedError()

    def _encode_tuple_2():
        raise NotImplementedError()

    def _encode_tuple_3():
        raise NotImplementedError()

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

    return _ENCODERS[type(entity)]()


def encode_i32(value: int):
    """Encodes a domain value: Signed 32 bit integer.
    
    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.I32].LENGTH, True)


def encode_i64(value: int):
    """Encodes a domain value: Signed 64 bit integer.
    
    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.I64].LENGTH, True)
    

def encode_key(value: str):
    """Encodes a domain value: A key mapping to data within global state.
    
    """
    return encode_string(value)


def encode_list(value: list):
    """Encodes a domain value: A list of values.
    
    """
    raise NotImplementedError()


def encode_map(value: list):
    """Encodes a domain value: A map of keys to associated values.
    
    """
    raise NotImplementedError()


def encode_option(value: object, inner_encoder: typing.Callable):
    """Encodes a domain value: An optional CL value.
    
    """
    return [0] if value is None else [1] + inner_encoder(value)


def encode_public_key(value: PublicKey):
    """Encodes a domain value: A public key.
    
    """
    return encode_string(value)


def encode_result(value: object):
    """Encodes a domain value: A smart contract execution result.
    
    """
    raise NotImplementedError()


def encode_string(value: str):
    """Encodes a domain value: A CL string.
    
    """
    value = encode_byte_array((value or "").encode("utf-8"))

    return encode_u32(len(value)) + value


def encode_tuple1(value: tuple):
    """Encodes a domain value: A 1-ary tuple of CL values.
    
    """
    raise NotImplementedError()


def encode_tuple2(value: tuple):
    """Encodes a domain value: A 2-ary tuple of CL values.
    
    """
    raise NotImplementedError()


def encode_tuple3(value: tuple):
    """Encodes a domain value: A 3-ary tuple of CL values.
    
    """
    raise NotImplementedError()


def encode_u8(value: int):
    """Encodes a domain value: Unsigned 8 bit integer.
    
    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH, False)


def encode_u8_array(value: typing.List[int]) -> typing.List[int]:
    """Encodes a domain value: Array of unsigned 8 bit integers.
    
    """
    return encode_u32(len(value)) + value


def encode_u32(value: int):
    """Encodes a domain value: Unsigned 32 bit integer.
    
    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH, False)


def encode_u64(value: int):
    """Encodes a domain value: Unsigned 64 bit integer.
    
    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH, False)


def encode_u128(value: int):
    """Encodes a domain value: Unsigned 128 bit integer.
    
    """
    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN or \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
        raise ValueError("Invalid U128: max size exceeded")
    
    if value >= NUMERIC_CONSTRAINTS[CLTypeKey.U8].MIN and \
       value <= NUMERIC_CONSTRAINTS[CLTypeKey.U8].MAX:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH
        type_key = CLTypeKey.U8

    elif value >= NUMERIC_CONSTRAINTS[CLTypeKey.U32].MIN and \
         value <= NUMERIC_CONSTRAINTS[CLTypeKey.U32].MAX:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH
        type_key = CLTypeKey.U32

    elif value >= NUMERIC_CONSTRAINTS[CLTypeKey.U64].MIN and \
         value <= NUMERIC_CONSTRAINTS[CLTypeKey.U64].MAX:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH
        type_key = CLTypeKey.U64

    else:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH
        type_key = CLTypeKey.U128
    
    return [type_key.value] + int_to_le_bytes_trimmed(value, encoded_length, False)


def encode_u256(value: int):
    """Encodes a domain value: Unsigned 256 bit integer.
    
    """
    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U256].MIN or \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U256].MAX:
        raise ValueError("Invalid U256: max size exceeded")

    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN and \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
        return [CLTypeKey.U256.value] + int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[CLTypeKey.U256].LENGTH, False)

    return encode_u128(value)


def encode_u512(value: int):
    """Encodes a domain value: Unsigned 512 bit integer.
    
    """
    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U512].MIN or \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U512].MAX:
        raise ValueError("Invalid U512: max size exceeded")

    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U256].MIN and \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U256].MAX:
        return [CLTypeKey.U512.value] + int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[CLTypeKey.U512].LENGTH, False)

    return encode_u256(value)


def encode_unit(value: None):
    """Encodes a domain value: A unitary CL value, i.e. a null.
    
    """
    return []


def encode_uref(value: str):
    """Encodes a domain value: An unforgeable reference.
    
    """
    return encode_byte_array((value or "").encode("utf-8"))


def encode_vector_of_t(value: list):
    """Encodes a domain value: An unbound vector.
    
    """
    return encode_u32(len(value)) + [i for j in value for i in j]


# Map: CL type <-> encoder.
_ENCODERS_CL = {
    CLTypeKey.ANY: encode_any,
    CLTypeKey.BOOL: encode_bool,
    CLTypeKey.BYTE_ARRAY: encode_byte_array,
    CLTypeKey.I32: encode_i32,
    CLTypeKey.I64: encode_i64,
    CLTypeKey.KEY: encode_key,
    CLTypeKey.LIST: encode_list,    
    CLTypeKey.MAP: encode_map,    
    CLTypeKey.OPTION: encode_option,    
    CLTypeKey.PUBLIC_KEY: encode_public_key,
    CLTypeKey.STRING: encode_string,
    CLTypeKey.TUPLE_1: encode_tuple1,
    CLTypeKey.TUPLE_2: encode_tuple2,
    CLTypeKey.TUPLE_3: encode_tuple3,
    CLTypeKey.U8: encode_u8,
    CLTypeKey.U32: encode_u32,
    CLTypeKey.U64: encode_u64,
    CLTypeKey.U128: encode_u128,    
    CLTypeKey.U256: encode_u256,
    CLTypeKey.U512: encode_u512,
    CLTypeKey.UNIT: encode_unit,
    CLTypeKey.RESULT: encode_result,
    CLTypeKey.UREF: encode_uref,
}


def encode(value: CLValue) -> typing.List[int]:
    """Encodes a domain value as an array of bytes.
    
    """
    encoder = _ENCODERS[value.cl_type.typeof]
    if value.cl_type.typeof == CLTypeKey.OPTION:
        inner_encoder = _ENCODERS[value.cl_type.inner_type.typeof]
        return encoder(value.parsed, inner_encoder)
    else:
        return encoder(value.parsed)
