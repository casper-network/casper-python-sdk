import typing

from pycspr import crypto
from pycspr.types import cl_types
from pycspr.types import cl_values
from pycspr.types import CL_TypeKey


def decode(
    bstream: bytes,
    cl_type: cl_types.CL_Type
) -> typing.Tuple[bytes, cl_values.CL_Value]:
    """Decodes a CL value from a byte array.

    :param bstream: An array of bytes being decoded.
    :param cl_type: CL type information.
    :returns: A CL value.

    """  
    try:
        decoder = _DECODERS[cl_type.type_key]
    except KeyError:
        raise ValueError(f"Unsupported CL value type: {cl_type.type_key}")
    else:
        return decoder(bstream, cl_type)


def _decode_any(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Any
) -> typing.Tuple[bytes, cl_values.CL_Any]:
    raise NotImplementedError()


def _decode_bool(bstream: bytes, _: cl_types.CL_Type_Bool = None) -> cl_values.CL_Bool:
    assert len(bstream) >= 1
    return bstream[1:], cl_values.CL_Bool(bool(bstream[0]))


def _decode_byte_array(
    bstream: bytes,
    cl_type: cl_types.CL_Type_ByteArray
) -> typing.Tuple[bytes, cl_values.CL_ByteArray]:
    assert len(bstream) >= cl_type.size
    bstream, encoded = bstream[cl_type.size:], bstream[:cl_type.size]

    return bstream, cl_values.CL_ByteArray(encoded)


def _decode_int(
    bstream: bytes,
    length: int,
    val_type: cl_values.CL_Value,
    signed: bool
) -> typing.Tuple[bytes, cl_values.CL_U8]:
    assert len(bstream) >= length
    bstream, encoded = bstream[length:], bstream[0:length]

    return bstream, val_type(int.from_bytes(encoded, "little", signed=signed))


def _decode_i32(
    bstream: bytes,
    _: cl_types.CL_Type_I32 = None
) -> typing.Tuple[bytes, cl_values.CL_I32]:
    return _decode_int(bstream, 4, cl_values.CL_I32, True)


def _decode_i64(
    bstream: bytes,
    _: cl_types.CL_Type_I64 = None
) -> typing.Tuple[bytes, cl_values.CL_I64]:
    return _decode_int(bstream, 8, cl_values.CL_I64, True)


def _decode_key(
    bstream: bytes,
    _: cl_types.CL_Type_Key = None
) -> typing.Tuple[bytes, cl_values.CL_Key]:
    assert len(bstream) >= 33
    key_type = cl_values.CL_KeyType(bstream[0])

    return bstream[33:], cl_values.CL_Key(bstream[1:33], key_type)


def _decode_list(
    bstream: bytes,
    cl_type: cl_types.CL_Type_List
) -> typing.Tuple[bytes, cl_values.CL_List]:
    bstream, size = _decode_i32(bstream, None)
    vector = []
    for _ in range(size.value):
        bstream, item = decode(bstream, cl_type.inner_type)
        vector.append(item)

    return bstream, cl_values.CL_List(vector)


def _decode_map(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Map
) -> typing.Tuple[bytes, cl_values.CL_Map]:
    bstream, size = _decode_i32(bstream, None)
    items = []
    for _ in range(size.value):
        bstream, key = decode(bstream, cl_type.key_type)
        bstream, val = decode(bstream, cl_type.value_type)
        items.append((key, val))

    return bstream, cl_values.CL_Map(items)


def _decode_option(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Option
) -> typing.Tuple[bytes, cl_values.CL_Option]:
    assert len(bstream) >= 1
    if bool(bstream[0]):
        bstream, decoded = decode(bstream[1:], cl_type.inner_type)
    else:
        bstream = bstream[1:]
        decoded = None

    return bstream, cl_values.CL_Option(decoded, cl_type.inner_type)


def _decode_public_key(
    bstream: bytes,
    _: cl_types.CL_Type_PublicKey
) -> typing.Tuple[bytes, cl_values.CL_PublicKey]:
    assert len(bstream) >= 1
    bstream, algo = bstream[1:], crypto.KeyAlgorithm(bstream[0])

    if algo == crypto.KeyAlgorithm.ED25519:
        key_length = 32
    elif algo == crypto.KeyAlgorithm.SECP256K1:
        key_length = 33
    else:
        raise ValueError("Unknown ecc key algorithm")
    assert len(bstream) >= key_length

    return bstream[key_length:], cl_values.CL_PublicKey(algo, bstream[0:key_length])


def _decode_result(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Result
) -> typing.Tuple[bytes, cl_values.CL_Result]:
    raise NotImplementedError()


def _decode_string(
    bstream: bytes,
    _: cl_types.CL_Type_String
) -> typing.Tuple[bytes, cl_values.CL_String]:
    bstream, size = _decode_i32(bstream, None)
    assert len(bstream) >= size.value
    bstream, encoded = bstream[size.value:], bstream[0:size.value]

    return bstream, cl_values.CL_String(encoded.decode("utf-8"))


def _decode_tuple_1(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Tuple1
) -> typing.Tuple[bytes, cl_values.CL_Tuple1]:
    bstream, v0 = decode(bstream, cl_type.t0_type)

    return bstream, cl_values.CL_Tuple1(v0)


def _decode_tuple_2(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Tuple2
) -> typing.Tuple[bytes, cl_values.CL_Tuple2]:
    bstream, v0 = decode(bstream, cl_type.t0_type)
    bstream, v1 = decode(bstream, cl_type.t1_type)

    return bstream, cl_values.CL_Tuple2(v0, v1)


def _decode_tuple_3(
    bstream: bytes,
    cl_type: cl_types.CL_Type_Tuple3
) -> typing.Tuple[bytes, cl_values.CL_Tuple3]:
    bstream, v0 = decode(bstream, cl_type.t0_type)
    bstream, v1 = decode(bstream, cl_type.t1_type)
    bstream, v2 = decode(bstream, cl_type.t2_type)

    return bstream, cl_values.CL_Tuple3(v0, v1, v2)


def _decode_u8(
    bstream: bytes,
    _: cl_types.CL_Type_U8 = None
) -> typing.Tuple[bytes, cl_values.CL_U8]:
    return _decode_int(bstream, 1, cl_values.CL_U8, False)


def _decode_u32(
    bstream: bytes,
    _: cl_types.CL_Type_U32 = None
) -> typing.Tuple[bytes, cl_values.CL_U32]:
    return _decode_int(bstream, 4, cl_values.CL_U32, False)


def _decode_u64(
    bstream: bytes,
    _: cl_types.CL_Type_U64 = None
) -> typing.Tuple[bytes, cl_values.CL_U64]:
    return _decode_int(bstream, 8, cl_values.CL_U64, False)


def _decode_u128(
    bstream: bytes,
    _: cl_types.CL_Type_U128 = None
) -> typing.Tuple[bytes, cl_values.CL_U128]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, cl_values.CL_U128, False)


def _decode_u256(
    bstream: bytes,
    _: cl_types.CL_Type_U256 = None
) -> typing.Tuple[bytes, cl_values.CL_U256]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, cl_values.CL_U256, False)


def _decode_u512(
    bstream: bytes,
    _: cl_types.CL_Type_U512 = None
) -> typing.Tuple[bytes, cl_values.CL_U512]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, cl_values.CL_U512, False)


def _decode_unit(
    bstream: bytes,
    _: cl_types.CL_Type_Unit = None
) -> typing.Tuple[bytes, cl_values.CL_Unit]:
    return bstream, cl_values.CL_Unit()


def _decode_uref(
    bstream: bytes,
    _: cl_types.CL_Type_URef = None
) -> typing.Tuple[bytes, cl_values.CL_URef]:
    assert len(bstream) >= 33
    bstream, encoded = bstream[33:], bstream[0:33]
    access_rights = cl_values.CL_URefAccessRights(encoded[-1])

    return bstream, cl_values.CL_URef(access_rights, encoded[:-1])


_DECODERS = {
    CL_TypeKey.ANY: _decode_any,
    CL_TypeKey.BOOL: _decode_bool,
    CL_TypeKey.BYTE_ARRAY: _decode_byte_array,
    CL_TypeKey.I32: _decode_i32,
    CL_TypeKey.I64: _decode_i64,
    CL_TypeKey.KEY: _decode_key,
    CL_TypeKey.LIST: _decode_list,
    CL_TypeKey.OPTION: _decode_option,
    CL_TypeKey.MAP: _decode_map,
    CL_TypeKey.PUBLIC_KEY: _decode_public_key,
    CL_TypeKey.RESULT: _decode_result,
    CL_TypeKey.STRING: _decode_string,
    CL_TypeKey.TUPLE_1: _decode_tuple_1,
    CL_TypeKey.TUPLE_2: _decode_tuple_2,
    CL_TypeKey.TUPLE_3: _decode_tuple_3,
    CL_TypeKey.U8: _decode_u8,
    CL_TypeKey.U32: _decode_u32,
    CL_TypeKey.U64: _decode_u64,
    CL_TypeKey.U128: _decode_u128,
    CL_TypeKey.U256: _decode_u256,
    CL_TypeKey.U512: _decode_u512,
    CL_TypeKey.UNIT: _decode_unit,
    CL_TypeKey.UREF: _decode_uref,
}
