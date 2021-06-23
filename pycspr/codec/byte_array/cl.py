import collections
import typing

from pycspr.codec.byte_array.utils import int_to_le_bytes
from pycspr.codec.byte_array.utils import int_to_le_bytes_trimmed
from pycspr.types.cl import CLTypeKey



NumericConstraints = collections.namedtuple("NumericConstraints", ["LENGTH", "MIN", "MAX"])

_NUMERIC_CONSTRAINTS ={
    CLTypeKey.I32: NumericConstraints(4, -(2 ** 32), (2 ** 32) - 1),
    CLTypeKey.I64: NumericConstraints(8, -(2 ** 64), (2 ** 64) - 1),
    CLTypeKey.U8: NumericConstraints(1, 0, (2 ** 8) - 1),
    CLTypeKey.U32: NumericConstraints(4, 0, (2 ** 32) - 1),
    CLTypeKey.U64: NumericConstraints(8, 0, (2 ** 64) - 1),
    CLTypeKey.U128: NumericConstraints(16, 0, (2 ** 128) - 1),
    CLTypeKey.U256: NumericConstraints(32, 0, (2 ** 256) - 1),
    CLTypeKey.U512: NumericConstraints(64, 0, (2 ** 512) - 1)
}


def encode_bool(value: bool):
    return [int(value)]


def encode_byte_array(value: typing.Union[bytes, str]):    
    if isinstance(value, str):
        return [int(i) for i in bytes.fromhex(value)]    
    else:
        return [int(i) for i in value]


def encode_i32(value: int):
    return int_to_le_bytes(value, _NUMERIC_CONSTRAINTS[CLTypeKey.I32].LENGTH, True)


def encode_i64(value: int):
    return int_to_le_bytes(value, _NUMERIC_CONSTRAINTS[CLTypeKey.I64].LENGTH, True)
    

def encode_key(value: str):
    return [int(i) for i in (value or "").encode("utf-8")]


def encode_list(value: list):
    return []


def encode_map(value: list):
    return []


def encode_option(value: object):
    if value is None:
        return [0]
    else:
        return [1] 
           # byte_array.encode(
            #     factory.cl_types.create_value(
            #         value.cl_type.inner_type,
            #         value.parsed
            #         )
            #     )

def encode_public_key(value: str):
    return [int(i) for i in (value or "").encode("utf-8")]


def encode_string(value: str):
    value = [int(i) for i in (value or "").encode("utf-8")]
    size = len(value)

    return encode_u32(size) + value


def encode_tuple1(value: tuple):
    return []


def encode_tuple2(value: tuple):
    return []


def encode_tuple3(value: tuple):
    return []


def encode_u8(value: int):
    return int_to_le_bytes(value, _NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH, False)


def encode_u8_array(value: typing.List[int]) -> typing.List[int]:
    return encode_u32(len(value)) + value


def encode_u32(value: int):
    return int_to_le_bytes(value, _NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH, False)


def encode_u64(value: int):
    return int_to_le_bytes(value, _NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH, False)


def encode_u128(value: int):
    if value < _NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN or \
       value > _NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
        raise ValueError("Invalid U128: max size exceeded")
    
    if value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U8].MIN and \
       value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U8].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH
        type_key = CLTypeKey.U8

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U32].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U32].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH
        type_key = CLTypeKey.U32

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U64].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U64].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH
        type_key = CLTypeKey.U64

    else:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH
        type_key = CLTypeKey.U128
    
    return [type_key.value] + int_to_le_bytes_trimmed(value, encoded_length, False)


def encode_u256(value: int):
    if value < _NUMERIC_CONSTRAINTS[CLTypeKey.U256].MIN or \
       value > _NUMERIC_CONSTRAINTS[CLTypeKey.U256].MAX:
        raise ValueError("Invalid U256: max size exceeded")
    
    if value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U8].MIN and \
       value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U8].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH
        type_key = CLTypeKey.U8

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U32].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U32].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH
        type_key = CLTypeKey.U32

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U64].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U64].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH
        type_key = CLTypeKey.U64

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH
        type_key = CLTypeKey.U128

    else:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U256].LENGTH
        type_key = CLTypeKey.U256
    
    return [type_key.value] + int_to_le_bytes_trimmed(value, encoded_length, False)


def encode_u512(value: int):
    if value < _NUMERIC_CONSTRAINTS[CLTypeKey.U512].MIN or \
       value > _NUMERIC_CONSTRAINTS[CLTypeKey.U512].MAX:
        raise ValueError("Invalid U512: max size exceeded")
    
    if value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U8].MIN and \
       value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U8].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH
        type_key = CLTypeKey.U8

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U32].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U32].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH
        type_key = CLTypeKey.U32

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U64].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U64].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH
        type_key = CLTypeKey.U64

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH
        type_key = CLTypeKey.U128

    elif value >= _NUMERIC_CONSTRAINTS[CLTypeKey.U256].MIN and \
         value <= _NUMERIC_CONSTRAINTS[CLTypeKey.U256].MAX:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U256].LENGTH
        type_key = CLTypeKey.U256

    else:
        encoded_length = _NUMERIC_CONSTRAINTS[CLTypeKey.U512].LENGTH
        type_key = CLTypeKey.U512
    
    return [type_key.value] + int_to_le_bytes_trimmed(value, encoded_length, False)


def encode_unit(value: None):
    return []


def encode_uref(value: str):
    return [int(i) for i in (value or "").encode("utf-8")]


def encode_vector_of_t(value: list):
    return encode_u32(len(value)) + [i for j in value for i in j]
