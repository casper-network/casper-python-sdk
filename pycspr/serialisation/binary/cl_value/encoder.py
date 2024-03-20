import typing

from pycspr.types.cl import CL_Value
from pycspr.types.cl import CL_Any
from pycspr.types.cl import CL_Bool
from pycspr.types.cl import CL_ByteArray
from pycspr.types.cl import CL_I32
from pycspr.types.cl import CL_I64
from pycspr.types.cl import CL_U8
from pycspr.types.cl import CL_U32
from pycspr.types.cl import CL_U64
from pycspr.types.cl import CL_U128
from pycspr.types.cl import CL_U256
from pycspr.types.cl import CL_U512
from pycspr.types.cl import CL_Key
from pycspr.types.cl import CL_List
from pycspr.types.cl import CL_Map
from pycspr.types.cl import CL_Option
from pycspr.types.cl import CL_PublicKey
from pycspr.types.cl import CL_Result
from pycspr.types.cl import CL_String
from pycspr.types.cl import CL_Tuple1
from pycspr.types.cl import CL_Tuple2
from pycspr.types.cl import CL_Tuple3
from pycspr.types.cl import CL_Unit
from pycspr.types.cl import CL_URef


def encode(entity: CL_Value) -> bytes:
    """Encoder: CL value -> array of bytes.

    :param entity: A CL value to be encoded.
    :returns: An array of bytes.

    """
    if type(entity) not in _ENCODERS:
        raise ValueError("CL value cannot be encoded as bytes")

    return _ENCODERS[type(entity)](entity)


def _encode_any(entity: CL_Any) -> bytes:
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


def _encode_list(entity: CL_List) -> bytes:
    return \
        encode(CL_U32(len(entity.vector))) + \
        bytes([i for j in map(encode, entity.vector) for i in j])


def _encode_map(entity: CL_Map) -> bytes:
    result = bytes([])
    for k, v in entity.value:
        result += encode(k)
        result += encode(v)

    return encode(CL_U32(len(entity.value))) + result


def _encode_result(entity: CL_Result) -> bytes:
    raise NotImplementedError()


def _encode_string(entity: CL_String) -> bytes:
    encoded: bytes = (entity.value or "").encode("utf-8")

    return encode(CL_U32(len(encoded))) + encoded


_ENCODERS = {
    CL_Any: _encode_any,
    CL_Bool: lambda x: bytes([x.value]),
    CL_ByteArray: lambda x: x.value,
    CL_I32: lambda x: _encode_int(x.value, (4, ), True, False),
    CL_I64: lambda x: _encode_int(x.value, (8, ), True, False),
    CL_Key: lambda x: bytes([x.key_type.value]) + x.identifier,
    CL_List: _encode_list,
    CL_Map: _encode_map,
    CL_Option: lambda x: bytes([1]) + encode(x.value) if x.value else bytes([0]),
    CL_PublicKey: lambda x: bytes([x.algo.value]) + x.pbk,
    CL_Result: _encode_result,
    CL_String: _encode_string,
    CL_Tuple1: lambda x: encode(x.v0),
    CL_Tuple2: lambda x: encode(x.v0) + encode(x.v1),
    CL_Tuple3: lambda x: encode(x.v0) + encode(x.v1) + encode(x.v2),
    CL_U8: lambda x: _encode_int(x.value, (1, ), False, False),
    CL_U32: lambda x: _encode_int(x.value, (4, ), False, False),
    CL_U64: lambda x: _encode_int(x.value, (8, ), False, False),
    CL_U128: lambda x: _encode_int(x.value, (1, 4, 8, 16), False, True),
    CL_U256: lambda x: _encode_int(x.value, (1, 4, 8, 16, 32), False, True),
    CL_U512: lambda x: _encode_int(x.value, (1, 4, 8, 16, 32, 64), False, True),
    CL_Unit: lambda _: bytes([]),
    CL_URef: lambda x: x.address + bytes([x.access_rights.value]),
}
