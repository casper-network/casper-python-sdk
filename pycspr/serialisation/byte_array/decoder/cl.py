import typing

from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLTypeKey
from pycspr.types import CLValue
from pycspr.types import PublicKey
from pycspr.utils.constants import NUMERIC_CONSTRAINTS
from pycspr.utils.conversion import le_bytes_to_int


def decode_any(as_bytes: typing.List[int]) -> object:
    """Decodes a value of an unassigned type.

    """
    raise NotImplementedError()


def decode_bool(as_bytes: typing.List[int]) -> bool:
    """Decodes a boolean.

    """
    return bool(as_bytes[0])


def decode_byte_array(as_bytes: typing.List[int]) -> bytes:
    """Decodes a byte array.

    """
    return bytes(as_bytes)


def decode_cl_value(as_bytes: typing.List[int]) -> CLValue:
    """Decodes a CL value.

    """
    raise NotImplementedError()


def decode_cl_type(entity: typing.List[int]) -> CLType:
    """Decodes a CL type definition.

    """
    raise NotImplementedError()


def decode_i32(as_bytes: typing.List[int]) -> int:
    """Decodes a signed 32 bit integer.

    """
    return le_bytes_to_int(as_bytes, True)


def decode_i64(as_bytes: typing.List[int]) -> int:
    """Decodes a signed 64 bit integer.

    """
    return le_bytes_to_int(as_bytes, True)


def decode_key(as_bytes: typing.List[int]) -> str:
    """Decodes a key mapping to data within global state.

    """
    raise NotImplementedError()


def decode_list(as_bytes: typing.List[int], inner_decoder: typing.Callable) -> list:
    """Decodes a list of values.

    """
    raise NotImplementedError()


def decode_map(as_bytes: typing.List[int]) -> dict:
    """Decodes a map of keys to associated values.

    """
    raise NotImplementedError()


def decode_option(as_bytes: typing.List[int], inner_cl_type: CLType):
    """Decodes an optional CL value.

    """
    is_defined, rem_bytes = bool(as_bytes[0]), as_bytes[1:]

    return decode(inner_cl_type, rem_bytes) if is_defined else None


def decode_public_key(as_bytes: typing.List[int]) -> PublicKey:
    """Decodes a public key.

    """
    raise NotImplementedError()


def decode_result(as_bytes: typing.List[int]):
    """Decodes a smart contract execution result.

    """
    raise NotImplementedError()


def decode_string(as_bytes: typing.List[int]) -> str:
    """Decodes a string.

    """
    raise NotImplementedError()


def decode_tuple1(as_bytes: typing.List[int]) -> tuple:
    """Decodes a 1-ary tuple of CL values.

    """
    raise NotImplementedError()


def decode_tuple2(as_bytes: typing.List[int]) -> tuple:
    """Decodes a 2-ary tuple of CL values.

    """
    raise NotImplementedError()


def decode_tuple3(as_bytes: typing.List[int]) -> tuple:
    """Decodes a 3-ary tuple of CL values.

    """
    raise NotImplementedError()


def decode_u8(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 8 bit integer.

    """
    return le_bytes_to_int(as_bytes, False)


def decode_u8_array(as_bytes: typing.List[int]) -> typing.List[int]:
    """Decodes an array of unsigned 8 bit integers.

    """
    raise NotImplementedError()


def decode_u32(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 32 bit integer.

    """
    return le_bytes_to_int(as_bytes, False)


def decode_u64(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 64 bit integer.

    """
    return le_bytes_to_int(as_bytes, False)


def decode_u128(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 128 bit integer.

    """
    size = as_bytes[0]
    if size <= NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH:
        return decode_u8(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH:
        return decode_u32(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH:
        return decode_u64(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH:
        return le_bytes_to_int(as_bytes[1:], False)
    else:
        raise ValueError("Cannot decode U128 as bytes are too large")


def decode_u256(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 256 bit integer.

    """
    size = as_bytes[0]
    if size <= NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH:
        return decode_u8(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH:
        return decode_u32(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH:
        return decode_u64(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH:
        return decode_u128(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U256].LENGTH:
        return le_bytes_to_int(as_bytes[1:], False)
    else:
        raise ValueError("Cannot decode U256 as bytes are too large")


def decode_u512(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 512 bit integer.

    """
    size = as_bytes[0]
    if size <= NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH:
        return decode_u8(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH:
        return decode_u32(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH:
        return decode_u64(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH:
        return decode_u128(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U256].LENGTH:
        return decode_u256(as_bytes[1:])
    elif size <= NUMERIC_CONSTRAINTS[CLTypeKey.U512].LENGTH:
        return le_bytes_to_int(as_bytes[1:], False)
    else:
        raise ValueError("Cannot decode U512 as bytes are too large")


def decode_unit(as_bytes: typing.List[int]) -> None:
    """Decodes a unitary CL value, i.e. a null.

    """
    raise NotImplementedError()


def decode_uref(as_bytes: typing.List[int]) -> str:
    """Decodes an unforgeable reference.

    """
    raise NotImplementedError()


def decode_vector_of_t(as_bytes: typing.List[int]) -> list:
    """Decodes an unbound vector.

    """
    raise NotImplementedError()


# Map: Simple type key <-> decoding function.
_SIMPLE_TYPE_DECODERS = {
    CLTypeKey.BOOL: decode_bool,
    CLTypeKey.I32: decode_i32,
    CLTypeKey.I64: decode_i64,
    CLTypeKey.KEY: decode_key,
    CLTypeKey.PUBLIC_KEY: decode_public_key,
    CLTypeKey.STRING: decode_string,
    CLTypeKey.U8: decode_u8,
    CLTypeKey.U32: decode_u32,
    CLTypeKey.U64: decode_u64,
    CLTypeKey.U128: decode_u128,
    CLTypeKey.U256: decode_u256,
    CLTypeKey.U512: decode_u512,
    CLTypeKey.UNIT: decode_unit,
    CLTypeKey.UREF: decode_uref,
}


def decode(type_info: CLType, as_bytes: typing.List[int]) -> typing.List[int]:
    """Decodes a domain entity from an array of bytes.

    """
    if isinstance(type_info, CLType_Simple):
        entity = _SIMPLE_TYPE_DECODERS[type_info.type_key](as_bytes)
    elif isinstance(type_info, CLType_ByteArray):
        entity = decode_byte_array(as_bytes)
    elif isinstance(type_info, CLType_Option):
        entity = decode_option(as_bytes, type_info.inner_type)
    else:
        entity = None

    return entity
