import typing

from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.cl_types import CLT_TypeKey
from pycspr.type_defs.cl_types import CLT_Any
from pycspr.type_defs.cl_types import CLT_Bool
from pycspr.type_defs.cl_types import CLT_ByteArray
from pycspr.type_defs.cl_types import CLT_I32
from pycspr.type_defs.cl_types import CLT_I64
from pycspr.type_defs.cl_types import CLT_U8
from pycspr.type_defs.cl_types import CLT_U32
from pycspr.type_defs.cl_types import CLT_U64
from pycspr.type_defs.cl_types import CLT_U128
from pycspr.type_defs.cl_types import CLT_U256
from pycspr.type_defs.cl_types import CLT_U512
from pycspr.type_defs.cl_types import CLT_Key
from pycspr.type_defs.cl_types import CLT_List
from pycspr.type_defs.cl_types import CLT_Map
from pycspr.type_defs.cl_types import CLT_Option
from pycspr.type_defs.cl_types import CLT_PublicKey
from pycspr.type_defs.cl_types import CLT_Result
from pycspr.type_defs.cl_types import CLT_String
from pycspr.type_defs.cl_types import CLT_Tuple1
from pycspr.type_defs.cl_types import CLT_Tuple2
from pycspr.type_defs.cl_types import CLT_Tuple3
from pycspr.type_defs.cl_types import CLT_Unit
from pycspr.type_defs.cl_types import CLT_URef
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
from pycspr.type_defs.cl_values import CLV_KeyType
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
from pycspr.type_defs.cl_values import CLV_URefAccessRights
from pycspr.type_defs.cl_values import CLV_URef
from pycspr.type_defs.crypto import KeyAlgorithm


def decode(typedef: CLT_Type, bstream: bytes) -> typing.Tuple[bytes, CLV_Value]:
    """Decoder: CL value <- an array of bytes.

    :param typedef: CL type information.
    :param bstream: An array of bytes to be decoded.
    :returns: A CL value.

    """
    try:
        decoder = _DECODERS[typedef.type_key]
    except KeyError:
        raise ValueError(f"Unsupported CL value type: {typedef.type_key}")
    else:
        return decoder(typedef, bstream)


def _decode_any(
    typedef: CLT_Any,
    bstream: bytes,
) -> typing.Tuple[bytes, CLV_Any]:
    raise NotImplementedError()


def _decode_bool(_: CLT_Bool, bstream: bytes) -> CLV_Bool:
    assert len(bstream) >= 1
    return bstream[1:], CLV_Bool(bool(bstream[0]))


def _decode_byte_array(
    typedef: CLT_ByteArray,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_ByteArray]:
    assert len(bstream) >= typedef.size
    bstream, encoded = bstream[typedef.size:], bstream[:typedef.size]

    return bstream, CLV_ByteArray(encoded)


def _decode_int(
    bstream: bytes,
    length: int,
    val_type: CLV_Value,
    signed: bool
) -> typing.Tuple[bytes, CLV_U8]:
    assert len(bstream) >= length
    bstream, encoded = bstream[length:], bstream[0:length]

    return bstream, val_type(int.from_bytes(encoded, "little", signed=signed))


def _decode_i32(
    _: CLT_I32,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_I32]:
    return _decode_int(bstream, 4, CLV_I32, True)


def _decode_i64(
    _: CLT_I64,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_I64]:
    return _decode_int(bstream, 8, CLV_I64, True)


def _decode_key(
    _: CLT_Key,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Key]:
    assert len(bstream) >= 33
    key_type = CLV_KeyType(bstream[0])

    return bstream[33:], CLV_Key(bstream[1:33], key_type)


def _decode_list(
    typedef: CLT_List,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_List]:
    print(typedef, bstream)
    bstream, size = _decode_i32(None, bstream)
    vector = []
    for _ in range(size.value):
        bstream, item = decode(typedef.inner_type, bstream)
        vector.append(item)

    return bstream, CLV_List(vector)


def _decode_map(
    typedef: CLT_Map,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Map]:
    bstream, size = _decode_i32(None, bstream)
    items = []
    for _ in range(size.value):
        bstream, key = decode(typedef.key_type, bstream)
        bstream, val = decode(typedef.value_type, bstream)
        items.append((key, val))

    return bstream, CLV_Map(items)


def _decode_option(
    typedef: CLT_Option,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Option]:
    assert len(bstream) >= 1
    if bool(bstream[0]):
        bstream, decoded = decode(typedef.inner_type, bstream[1:])
    else:
        bstream = bstream[1:]
        decoded = None

    return bstream, CLV_Option(decoded, typedef.inner_type)


def _decode_public_key(
    _: CLT_PublicKey,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_PublicKey]:
    assert len(bstream) >= 1
    bstream, algo = bstream[1:], KeyAlgorithm(bstream[0])

    if algo == KeyAlgorithm.ED25519:
        key_length = 32
    elif algo == KeyAlgorithm.SECP256K1:
        key_length = 33
    else:
        raise ValueError("Unknown ecc key algorithm")
    assert len(bstream) >= key_length

    return bstream[key_length:], CLV_PublicKey(algo, bstream[0:key_length])


def _decode_result(
    typedef: CLT_Result,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Result]:
    raise NotImplementedError()


def _decode_string(
    _: CLT_String,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_String]:
    bstream, size = _decode_i32(None, bstream)
    assert len(bstream) >= size.value
    bstream, encoded = bstream[size.value:], bstream[0:size.value]

    return bstream, CLV_String(encoded.decode("utf-8"))


def _decode_tuple_1(
    typedef: CLT_Tuple1,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Tuple1]:
    bstream, v0 = decode(typedef.t0_type, bstream)

    return bstream, CLV_Tuple1(v0)


def _decode_tuple_2(
    typedef: CLT_Tuple2,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Tuple2]:
    bstream, v0 = decode(typedef.t0_type, bstream)
    bstream, v1 = decode(typedef.t1_type, bstream)

    return bstream, CLV_Tuple2(v0, v1)


def _decode_tuple_3(
    typedef: CLT_Tuple3,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Tuple3]:
    bstream, v0 = decode(typedef.t0_type, bstream)
    bstream, v1 = decode(typedef.t1_type, bstream)
    bstream, v2 = decode(typedef.t2_type, bstream)

    return bstream, CLV_Tuple3(v0, v1, v2)


def _decode_u8(
    _: CLT_U8,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_U8]:
    return _decode_int(bstream, 1, CLV_U8, False)


def _decode_u32(
    _: CLT_U32,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_U32]:
    return _decode_int(bstream, 4, CLV_U32, False)


def _decode_u64(
    _: CLT_U64,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_U64]:
    return _decode_int(bstream, 8, CLV_U64, False)


def _decode_u128(
    _: CLT_U128,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_U128]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, CLV_U128, False)


def _decode_u256(
    _: CLT_U256,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_U256]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, CLV_U256, False)


def _decode_u512(
    _: CLT_U512,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_U512]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, CLV_U512, False)


def _decode_unit(
    _: CLT_Unit,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_Unit]:
    return bstream, CLV_Unit()


def _decode_uref(
    _: CLT_URef,
    bstream: bytes
) -> typing.Tuple[bytes, CLV_URef]:
    assert len(bstream) >= 33
    bstream, encoded = bstream[33:], bstream[0:33]
    access_rights = CLV_URefAccessRights(encoded[-1])

    return bstream, CLV_URef(access_rights, encoded[:-1])


_DECODERS = {
    CLT_TypeKey.ANY: _decode_any,
    CLT_TypeKey.BOOL: _decode_bool,
    CLT_TypeKey.BYTE_ARRAY: _decode_byte_array,
    CLT_TypeKey.I32: _decode_i32,
    CLT_TypeKey.I64: _decode_i64,
    CLT_TypeKey.KEY: _decode_key,
    CLT_TypeKey.LIST: _decode_list,
    CLT_TypeKey.OPTION: _decode_option,
    CLT_TypeKey.MAP: _decode_map,
    CLT_TypeKey.PUBLIC_KEY: _decode_public_key,
    CLT_TypeKey.RESULT: _decode_result,
    CLT_TypeKey.STRING: _decode_string,
    CLT_TypeKey.TUPLE_1: _decode_tuple_1,
    CLT_TypeKey.TUPLE_2: _decode_tuple_2,
    CLT_TypeKey.TUPLE_3: _decode_tuple_3,
    CLT_TypeKey.U8: _decode_u8,
    CLT_TypeKey.U32: _decode_u32,
    CLT_TypeKey.U64: _decode_u64,
    CLT_TypeKey.U128: _decode_u128,
    CLT_TypeKey.U256: _decode_u256,
    CLT_TypeKey.U512: _decode_u512,
    CLT_TypeKey.UNIT: _decode_unit,
    CLT_TypeKey.UREF: _decode_uref,
}
