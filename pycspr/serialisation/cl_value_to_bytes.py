from pycspr.types import cl_values
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import int_to_le_bytes_trimmed


def encode(entity: cl_values.CL_Value) -> bytes:
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("CL value cannot be encoded as bytes")
    else:
        return encoder(entity)


def encode_any(entity: cl_values.CL_Any) -> bytes:
    raise NotImplementedError()


def encode_bool(entity: cl_values.CL_Bool) -> bytes:
    return bytes([entity.value])


def encode_byte_array(entity: cl_values.CL_ByteArray) -> bytes:
    return entity.value


def encode_i32(entity: cl_values.CL_I32) -> bytes:
    return int_to_le_bytes(entity.value, 4, True)


def encode_i64(entity: cl_values.CL_I64) -> bytes:
    return int_to_le_bytes(entity.value, 8, True)


def encode_key(entity: cl_values.CL_Key) -> bytes:
    return bytes([entity.key_type.value]) + entity.identifier


def encode_list(entity: cl_values.CL_List) -> bytes:
    return \
        encode(cl_values.CL_U32(len(entity.vector))) + \
        bytes([i for j in map(encode, entity.vector) for i in j])


def encode_map(entity: cl_values.CL_Map) -> bytes:
    result = bytes([])
    for k, v in entity.value:
        result += encode(k) 
        result += encode(v) 

    return encode(cl_values.CL_U32(len(entity.value))) + result


def encode_option(entity: cl_values.CL_Option) -> bytes:
    return bytes([1]) + encode(entity.value) if entity.value else bytes([0])


def encode_public_key(entity: cl_values.CL_PublicKey) -> bytes:
    return bytes([entity.algo.value]) + entity.pbk


def encode_result(entity: cl_values.CL_Result) -> bytes:
    raise NotImplementedError()


def encode_string(entity: cl_values.CL_String) -> bytes:
    encoded: bytes = (entity.value or "").encode("utf-8")
    return encode(cl_values.CL_U32(len(encoded))) + encoded


def encode_tuple_1(entity: cl_values.CL_Tuple1) -> bytes:
    return encode(entity.v0)


def encode_tuple_2(entity: cl_values.CL_Tuple2) -> bytes:
    return encode(entity.v0) + encode(entity.v1)


def encode_tuple_3(entity: cl_values.CL_Tuple3) -> bytes:
    return encode(entity.v0) + encode(entity.v1) + encode(entity.v2)


def encode_u8(entity: cl_values.CL_U8) -> bytes:
    return int_to_le_bytes(entity.value, 1, False)


def encode_u32(entity: cl_values.CL_U32) -> bytes:
    return int_to_le_bytes(entity.value, 4, False)


def encode_u64(entity: cl_values.CL_U64) -> bytes:
    return int_to_le_bytes(entity.value, 8, False)


def encode_u128(entity: cl_values.CL_U128) -> bytes:
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


def encode_u256(entity: cl_values.CL_U256) -> bytes:
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

    # int.from_bytes(bytes([128]), "little", signed=False)


def encode_u512(entity: cl_values.CL_U512) -> bytes:
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


def encode_unit(entity: cl_values.CL_Unit) -> bytes:
    return bytes([])


def encode_uref(entity: cl_values.CL_URef) -> bytes:
    return entity.address + bytes([entity.access_rights.value])


_ENCODERS = {
    cl_values.CL_Any: encode_any,
    cl_values.CL_Bool: encode_bool,
    cl_values.CL_ByteArray: encode_byte_array,
    cl_values.CL_I32: encode_i32,
    cl_values.CL_I64: encode_i64,
    cl_values.CL_Key: encode_key,
    cl_values.CL_List: encode_list,
    cl_values.CL_Map: encode_map,
    cl_values.CL_Option: encode_option,
    cl_values.CL_PublicKey: encode_public_key,
    cl_values.CL_Result: encode_result,
    cl_values.CL_String: encode_string,
    cl_values.CL_Tuple1: encode_tuple_1,
    cl_values.CL_Tuple2: encode_tuple_2,
    cl_values.CL_Tuple3: encode_tuple_3,
    cl_values.CL_U8: encode_u8,
    cl_values.CL_U32: encode_u32,
    cl_values.CL_U64: encode_u64,
    cl_values.CL_U128: encode_u128,
    cl_values.CL_U256: encode_u256,
    cl_values.CL_U512: encode_u512,
    cl_values.CL_Unit: encode_unit,
    cl_values.CL_URef: encode_uref,
}
