import typing

from pycspr.types import cl_values


def encode(entity: cl_values.CL_Value) -> bytes:
    """Encodes a CL value as an array of bytes.

    :param entity: A CL value to be encoded.
    :returns: An array of bytes.
    
    """    
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


def _encode_int(
    value: int,
    byte_lengths: typing.List[int],
    signed: bool,
    trim: bool
) -> bytes:
    encoded = None
    for length in byte_lengths:
        try:
            encoded = value.to_bytes(length, "little", signed=signed)
        except OverflowError:
            continue
    
    if encoded is None:
        raise ValueError("Invalid integer: max size exceeded")

    if trim:
        while encoded and encoded[-1] == 0:
            encoded = encoded[0:-1]

    if len(byte_lengths) == 1:
        return encoded
    else:
        return bytes([len(encoded)]) + encoded


def _encode_i32(entity: cl_values.CL_I32) -> bytes:
    return _encode_int(entity.value, (4, ), signed=True, trim=False)


def _encode_i64(entity: cl_values.CL_I64) -> bytes:
    return _encode_int(entity.value, (8, ), signed=True, trim=False)


def _encode_key(entity: cl_values.CL_Key) -> bytes:
    return bytes([entity.key_type.value]) + entity.identifier


def _encode_list(entity: cl_values.CL_List) -> bytes:
    return \
        encode(cl_values.CL_U32(len(entity.vector))) + \
        bytes([i for j in map(encode, entity.vector) for i in j])


def _encode_map(entity: cl_values.CL_Map) -> bytes:
    result = bytes([])
    for k, v in entity.value:
        result += encode(k)
        result += encode(v)

    return encode(cl_values.CL_U32(len(entity.value))) + result


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
    return encode(entity.v0)


def _encode_tuple_2(entity: cl_values.CL_Tuple2) -> bytes:
    return encode(entity.v0) + encode(entity.v1)


def _encode_tuple_3(entity: cl_values.CL_Tuple3) -> bytes:
    return encode(entity.v0) + encode(entity.v1) + encode(entity.v2)


def _encode_u8(entity: cl_values.CL_U8) -> bytes:
    return _encode_int(entity.value, (1, ), signed=False, trim=False)


def _encode_u32(entity: cl_values.CL_U32) -> bytes:
    return _encode_int(entity.value, (4, ), signed=False, trim=False)


def _encode_u64(entity: cl_values.CL_U64) -> bytes:
    return _encode_int(entity.value, (8, ), signed=False, trim=False)


def _encode_u128(entity: cl_values.CL_U128) -> bytes:
    return _encode_int(entity.value, (1, 4, 8, 16), signed=False, trim=True)


def _encode_u256(entity: cl_values.CL_U256) -> bytes:
    return _encode_int(entity.value, (1, 4, 8, 16, 32), signed=False, trim=True)


def _encode_u512(entity: cl_values.CL_U512) -> bytes:
    return _encode_int(entity.value, (1, 4, 8, 16, 32, 64), signed=False, trim=True)


def _encode_unit(_: cl_values.CL_Unit) -> bytes:
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
