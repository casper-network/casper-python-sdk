import typing

from pycspr.type_defs.cl_values import CLV_Value
from pycspr.type_defs.cl_values import CLV_Any
from pycspr.type_defs.cl_values import CLV_Bool
from pycspr.type_defs.cl_values import CLV_ByteArray
from pycspr.type_defs.cl_values import CLV_I32
from pycspr.type_defs.cl_values import CLV_I64
from pycspr.type_defs.cl_values import CLV_U8
from pycspr.type_defs.cl_values import CLV_U32
from pycspr.type_defs.cl_values import CLV_U64
from pycspr.type_defs.cl_values import CLV_U128
from pycspr.type_defs.cl_values import CLV_U256
from pycspr.type_defs.cl_values import CLV_U512
from pycspr.type_defs.cl_values import CLV_Key
from pycspr.type_defs.cl_values import CLV_List
from pycspr.type_defs.cl_values import CLV_Map
from pycspr.type_defs.cl_values import CLV_Option
from pycspr.type_defs.cl_values import CLV_PublicKey
from pycspr.type_defs.cl_values import CLV_Result
from pycspr.type_defs.cl_values import CLV_String
from pycspr.type_defs.cl_values import CLV_Tuple1
from pycspr.type_defs.cl_values import CLV_Tuple2
from pycspr.type_defs.cl_values import CLV_Tuple3
from pycspr.type_defs.cl_values import CLV_Unit
from pycspr.type_defs.cl_values import CLV_URef


def encode(entity: CLV_Value) -> bytes:
    """Encoder: CL value -> array of bytes.

    :param entity: A CL value to be encoded.
    :returns: An array of bytes.

    """
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"CL value cannot be encoded as bytes: {type(entity)}")
    else:
        return encoder(entity)


def _encode_any(entity: CLV_Any) -> bytes:
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


def _encode_list(entity: CLV_List) -> bytes:
    return \
        encode(CLV_U32(len(entity.vector))) + \
        bytes([i for j in map(encode, entity.vector) for i in j])


def _encode_map(entity: CLV_Map) -> bytes:
    result = bytes([])
    for k, v in entity.value:
        result += encode(k)
        result += encode(v)

    return encode(CLV_U32(len(entity.value))) + result


def _encode_result(entity: CLV_Result) -> bytes:
    raise NotImplementedError()


def _encode_string(entity: CLV_String) -> bytes:
    encoded: bytes = (entity.value or "").encode("utf-8")

    return encode(CLV_U32(len(encoded))) + encoded


_ENCODERS = {
    CLV_Any: _encode_any,
    CLV_Bool: lambda x: bytes([x.value]),
    CLV_ByteArray: lambda x: x.value,
    CLV_I32: lambda x: _encode_int(x.value, (4, ), True, False),
    CLV_I64: lambda x: _encode_int(x.value, (8, ), True, False),
    CLV_Key: lambda x: bytes([x.key_type.value]) + x.identifier,
    CLV_List: _encode_list,
    CLV_Map: _encode_map,
    CLV_Option: lambda x: bytes([1]) + encode(x.value) if x.value else bytes([0]),
    CLV_PublicKey: lambda x: bytes([x.algo.value]) + x.pbk,
    CLV_Result: _encode_result,
    CLV_String: _encode_string,
    CLV_Tuple1: lambda x: encode(x.v0),
    CLV_Tuple2: lambda x: encode(x.v0) + encode(x.v1),
    CLV_Tuple3: lambda x: encode(x.v0) + encode(x.v1) + encode(x.v2),
    CLV_U8: lambda x: _encode_int(x.value, (1, ), False, False),
    CLV_U32: lambda x: _encode_int(x.value, (4, ), False, False),
    CLV_U64: lambda x: _encode_int(x.value, (8, ), False, False),
    CLV_U128: lambda x: _encode_int(x.value, (1, 4, 8, 16), False, True),
    CLV_U256: lambda x: _encode_int(x.value, (1, 4, 8, 16, 32), False, True),
    CLV_U512: lambda x: _encode_int(x.value, (1, 4, 8, 16, 32, 64), False, True),
    CLV_Unit: lambda _: bytes([]),
    CLV_URef: lambda x: x.address + bytes([x.access_rights.value]),
}
