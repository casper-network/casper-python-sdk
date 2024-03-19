import typing

from pycspr.types import cl_values


def encode(entity: cl_values.CL_Value) -> bytes:
    """Encoder: CL value -> array of bytes.

    :param entity: A CL value to be encoded.
    :returns: An array of bytes.

    """
    if type(entity) not in _ENCODERS:
        raise ValueError("CL value cannot be encoded as bytes")

    return _ENCODERS[type(entity)](entity)


def _encode_any(entity: cl_values.CL_Any) -> bytes:
    raise NotImplementedError()


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


def _encode_result(entity: cl_values.CL_Result) -> bytes:
    raise NotImplementedError()


def _encode_string(entity: cl_values.CL_String) -> bytes:
    encoded: bytes = (entity.value or "").encode("utf-8")

    return encode(cl_values.CL_U32(len(encoded))) + encoded


_ENCODERS = {
    cl_values.CL_Any: _encode_any,
    cl_values.CL_Bool: lambda x: bytes([x.value]),
    cl_values.CL_ByteArray: lambda x: x.value,
    cl_values.CL_I32: lambda x: _encode_int(x.value, (4, ), True, False),
    cl_values.CL_I64: lambda x: _encode_int(x.value, (8, ), True, False),
    cl_values.CL_Key: lambda x: bytes([x.key_type.value]) + x.identifier,
    cl_values.CL_List: _encode_list,
    cl_values.CL_Map: _encode_map,
    cl_values.CL_Option: lambda x: bytes([1]) + encode(x.value) if x.value else bytes([0]),
    cl_values.CL_PublicKey: lambda x: bytes([x.algo.value]) + x.pbk,
    cl_values.CL_Result: _encode_result,
    cl_values.CL_String: _encode_string,
    cl_values.CL_Tuple1: lambda x: encode(x.v0),
    cl_values.CL_Tuple2: lambda x: encode(x.v0) + encode(x.v1),
    cl_values.CL_Tuple3: lambda x: encode(x.v0) + encode(x.v1) + encode(x.v2),
    cl_values.CL_U8: lambda x: _encode_int(x.value, (1, ), False, False),
    cl_values.CL_U32: lambda x: _encode_int(x.value, (4, ), False, False),
    cl_values.CL_U64: lambda x: _encode_int(x.value, (8, ), False, False),
    cl_values.CL_U128: lambda x: _encode_int(x.value, (1, 4, 8, 16), False, True),
    cl_values.CL_U256: lambda x: _encode_int(x.value, (1, 4, 8, 16, 32), False, True),
    cl_values.CL_U512: lambda x: _encode_int(x.value, (1, 4, 8, 16, 32, 64), False, True),
    cl_values.CL_Unit: lambda _: bytes([]),
    cl_values.CL_URef: lambda x: x.address + bytes([x.access_rights.value]),
}
