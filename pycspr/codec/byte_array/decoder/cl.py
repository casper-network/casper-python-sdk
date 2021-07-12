import typing

from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLTypeKey
from pycspr.types import CLType_Option
from pycspr.types import CLValue
from pycspr.types import PublicKey



def decode_any(as_bytes: typing.List[int]) -> object:
    """Decodes a value of an unassigned type.
    
    """
    raise NotImplementedError()


def decode_bool(as_bytes: typing.List[int]) -> bool:
    """Decodes a boolean.
    
    """
    raise NotImplementedError()


def decode_byte_array(as_bytes: typing.List[int]) -> bytes:    
    """Decodes a byte array.
    
    """
    raise NotImplementedError()


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
    raise NotImplementedError()


def decode_i64(as_bytes: typing.List[int]) -> int:
    """Decodes a signed 64 bit integer.
    
    """
    raise NotImplementedError()    


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


def decode_option(as_bytes: typing.List[int], inner_decoder: typing.Callable):
    """Decodes an optional CL value.
    
    """
    raise NotImplementedError()


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
    raise NotImplementedError()


def decode_u8_array(as_bytes: typing.List[int]) -> typing.List[int]:
    """Decodes an array of unsigned 8 bit integers.
    
    """
    raise NotImplementedError()


def decode_u32(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 32 bit integer.
    
    """
    raise NotImplementedError()


def decode_u64(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 64 bit integer.
    
    """
    raise NotImplementedError()


def decode_u128(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 128 bit integer.
    
    """
    raise NotImplementedError()


def decode_u256(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 256 bit integer.
    
    """
    raise NotImplementedError()


def decode_u512(as_bytes: typing.List[int]) -> int:
    """Decodes an unsigned 512 bit integer.
    
    """
    print(len(as_bytes), as_bytes.hex(), int(as_bytes[0]), as_bytes)

    raise NotImplementedError()


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
    CLTypeKey.STRING: decode_option,
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
    """Decodes a domain value from an array of bytes.
    
    """
    if isinstance(type_info, CLType_Simple):
        return _SIMPLE_TYPE_DECODERS[type_info.typeof](as_bytes)
    else:
        print(type_info, as_bytes)
        return None
