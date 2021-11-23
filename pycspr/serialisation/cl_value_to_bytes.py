import typing

from pycspr.types.cl import cl_values
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import int_to_le_bytes_trimmed


def encode(entity: cl_values.CL_Value) -> bytes:
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("CL value cannot be encoded as bytes")
    else:
        return encoder(entity)


def _encode_any(entity: cl_values.CL_Any) -> bytes:
    raise NotImplementedError()


def _encode_bool(entity: cl_values.CL_Bool) -> bytes:
    return bytes([entity.value])


def _encode_byte_array(entity: cl_values.CL_ByteArray) -> bytes:
    return entity.value


def _encode_i32(entity: cl_values.CL_I32) -> bytes:
    return int_to_le_bytes(entity.value, 4, True)


def _encode_i64(entity: cl_values.CL_I64) -> bytes:
    return int_to_le_bytes(entity.value, 8, True)


def _encode_key(entity: cl_values.CL_Key) -> bytes:
    return bytes([entity.key_type.value]) + entity.identifier


def _encode_list(entity: cl_values.CL_List) -> bytes:
    return _vector_to_bytes(list(map(encode, entity.vector)))


def _encode_map(entity: cl_values.CL_Map) -> bytes:
    raise NotImplementedError()


def _encode_option(entity: cl_values.CL_Option) -> bytes:
    return bytes([1]) + encode(entity.value) if entity.value else bytes([0])


def _encode_public_key(entity: cl_values.CL_PublicKey) -> bytes:
    return bytes([entity.algo.value]) + entity.pbk


def _encode_result(entity: cl_values.CL_Result) -> bytes:
    raise NotImplementedError()


def _encode_string(entity: cl_values.CL_String) -> bytes:
    encoded: bytes = (entity.value or "").encode("utf-8")
    return encode(cl_values.CL_U32(len(encoded))) + encoded


def _encode_tuple_1(entity: cl_values.CL_Tuple1) -> bytes:
    raise NotImplementedError()


def _encode_tuple_2(entity: cl_values.CL_Tuple2) -> bytes:
    raise NotImplementedError()


def _encode_tuple_3(entity: cl_values.CL_Tuple3) -> bytes:
    raise NotImplementedError()


def _encode_u8(entity: cl_values.CL_U8) -> bytes:
    return int_to_le_bytes(entity.value, 1, False)


def _encode_u32(entity: cl_values.CL_U32) -> bytes:
    return int_to_le_bytes(entity.value, 4, False)


def _encode_u64(entity: cl_values.CL_U64) -> bytes:
    return int_to_le_bytes(entity.value, 8, False)


def _encode_u128(entity: cl_values.CL_U128) -> bytes:
    if cl_values.CL_U8.is_in_range(entity.value):
        byte_length = 1
    elif cl_values.CL_U32.is_in_range(entity.value):
        byte_length = 4
    elif cl_values.CL_U64.is_in_range(entity.value):
        byte_length = 8
    elif cl_values.CL_U128.is_in_range(entity.value):
        byte_length = 16
    else:
        raise ValueError("Invalid U128: max size exceeded")

    as_bytes = int_to_le_bytes_trimmed(entity.value, byte_length, False)

    return bytes([len(as_bytes)]) + as_bytes


def _encode_u256(entity: cl_values.CL_U256) -> bytes:
    if cl_values.CL_U8.is_in_range(entity.value):
        byte_length = 1
    elif cl_values.CL_U32.is_in_range(entity.value):
        byte_length = 4
    elif cl_values.CL_U64.is_in_range(entity.value):
        byte_length = 8
    elif cl_values.CL_U128.is_in_range(entity.value):
        byte_length = 16
    elif cl_values.CL_U256.is_in_range(entity.value):
        byte_length = 32
    else:
        raise ValueError("Invalid U256: max size exceeded")

    as_bytes = int_to_le_bytes_trimmed(entity.value, byte_length, False)

    return bytes([len(as_bytes)]) + as_bytes


def _encode_u512(entity: cl_values.CL_U512) -> bytes:
    if cl_values.CL_U8.is_in_range(entity.value):
        byte_length = 1
    elif cl_values.CL_U32.is_in_range(entity.value):
        byte_length = 4
    elif cl_values.CL_U64.is_in_range(entity.value):
        byte_length = 8
    elif cl_values.CL_U128.is_in_range(entity.value):
        byte_length = 16
    elif cl_values.CL_U256.is_in_range(entity.value):
        byte_length = 32
    elif cl_values.CL_U512.is_in_range(entity.value):
        byte_length = 64
    else:
        raise ValueError("Invalid U512: max size exceeded")

    as_bytes = int_to_le_bytes_trimmed(entity.value, byte_length, False)

    return bytes([len(as_bytes)]) + as_bytes


def _encode_unit(entity: cl_values.CL_Unit) -> bytes:
    return bytes([])


def _encode_uref(entity: cl_values.CL_URef) -> bytes:
    return entity.address + bytes([entity.access_rights.value])


_ENCODERS = {
    cl_values.CL_Any: _encode_any,
    cl_values.CL_Bool: _encode_bool,
    cl_values.CL_ByteArray: _encode_byte_array,
    cl_values.CL_I32: _encode_i32,
    cl_values.CL_I64: _encode_i64,
    cl_values.CL_Key: _encode_key,
    cl_values.CL_List: _encode_list,
    cl_values.CL_Map: _encode_map,
    cl_values.CL_Option: _encode_option,
    cl_values.CL_PublicKey: _encode_public_key,
    cl_values.CL_Result: _encode_result,
    cl_values.CL_String: _encode_string,
    cl_values.CL_Tuple1: _encode_tuple_1,
    cl_values.CL_Tuple2: _encode_tuple_2,
    cl_values.CL_Tuple3: _encode_tuple_3,
    cl_values.CL_U8: _encode_u8,
    cl_values.CL_U32: _encode_u32,
    cl_values.CL_U64: _encode_u64,
    cl_values.CL_U128: _encode_u128,
    cl_values.CL_U256: _encode_u256,
    cl_values.CL_U512: _encode_u512,
    cl_values.CL_Unit: _encode_unit,
    cl_values.CL_URef: _encode_uref,
}


def _vector_to_bytes(value: typing.List) -> bytes:
    return \
        encode(cl_values.CL_U32(len(value))) + \
        bytes([i for j in value for i in j])
