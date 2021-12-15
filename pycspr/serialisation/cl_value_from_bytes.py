import typing

from pycspr import crypto
from pycspr.types import CL_TYPEKEY_TO_CL_VALUE_TYPE
from pycspr.types import cl_types
from pycspr.types import cl_values



def decode(bstream: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Value]:
    cl_value_type: cl_values.CL_Value = CL_TYPEKEY_TO_CL_VALUE_TYPE[cl_type.type_key]
    try:
        decoder = _DECODERS[cl_value_type]
    except KeyError:
        raise ValueError(f"Unsupported CL value type: {cl_value_type}")

    return decoder(bstream, cl_type)


def _decode_any(encoded: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Any]:
    raise NotImplementedError()


def _decode_bool(bstream: bytes, _: cl_types.CL_Type) -> cl_values.CL_Bool:
    assert len(bstream) >= 1
    return bstream[1:], cl_values.CL_Bool(bool(bstream[0]))


def _decode_byte_array(bstream: bytes, cl_type: cl_types.CL_Type_ByteArray) -> typing.Tuple[bytes, cl_values.CL_ByteArray]:
    assert len(bstream) >= cl_type.size
    bstream, encoded = bstream[cl_type.size:], bstream[:cl_type.size]

    return bstream, cl_values.CL_ByteArray(encoded)


def _decode_int(bstream: bytes, length: int, val_type: cl_values.CL_Value, signed: bool) -> typing.Tuple[bytes, cl_values.CL_U8]:
    assert len(bstream) >= length
    bstream, encoded = bstream[length:], bstream[0:length]

    return bstream, val_type(int.from_bytes(encoded, "little", signed=signed))


def _decode_i32(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_I32]:
    return _decode_int(bstream, 4, cl_values.CL_I32, True)


def _decode_i64(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_I64]:
    return _decode_int(bstream, 8, cl_values.CL_I64, True)


def _decode_key(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Key]:
    assert len(bstream) >= 33
    key_type = cl_values.CL_KeyType(bstream[0])

    return bstream[33:], cl_values.CL_Key(bstream[1:33], key_type)
    

def _decode_list(bstream: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_List]:
    raise NotImplementedError()


def _decode_map(bstream: bytes, cl_type: cl_types.CL_Type_Map) -> typing.Tuple[bytes, cl_values.CL_Map]:
    bstream, size = _decode_i32(bstream, None)    
    items = []
    for _ in range(size.value):    
        bstream, key = decode(bstream, cl_type.key_type)
        bstream, val = decode(bstream, cl_type.value_type)           
        items.append((key, val))

    return bstream, cl_values.CL_Map(items)


def _decode_option(bstream: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Option]:
    assert len(bstream) >= 1
    if bool(bstream[0]) == True:
        bstream, decoded = decode(bstream[1:], cl_type.inner_type)
    else:
        bstream = bstream[1:]
        decoded = None

    return bstream, cl_values.CL_Option(decoded, cl_type.inner_type)


def _decode_public_key(bstream: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_PublicKey]:
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


def _decode_result(encoded: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Result]:
    raise NotImplementedError()


def _decode_string(bstream: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_String]:
    bstream, size = _decode_i32(bstream, None)
    assert len(bstream) >= size.value    
    bstream, encoded = bstream[size.value:], bstream[0:size.value]

    return bstream, cl_values.CL_String(encoded.decode("utf-8"))


def _decode_tuple_1(encoded: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Tuple1]:
    raise NotImplementedError()


def _decode_tuple_2(encoded: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Tuple2]:
    raise NotImplementedError()


def _decode_tuple_3(encoded: bytes, cl_type: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Tuple3]:
    raise NotImplementedError()


def _decode_u8(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_U8]:
    return _decode_int(bstream, 1, cl_values.CL_U8, False)


def _decode_u32(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_U32]:
    return _decode_int(bstream, 4, cl_values.CL_U32, False)


def _decode_u64(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_U64]:
    return _decode_int(bstream, 8, cl_values.CL_U64, False)


def _decode_u128(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_U128]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, cl_values.CL_U128, False)


def _decode_u256(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_U256]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, cl_values.CL_U256, False)


def _decode_u512(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_U512]:
    assert len(bstream) >= 1
    bstream, length = bstream[1:], bstream[0]

    return _decode_int(bstream, length, cl_values.CL_U512, False)


def _decode_unit(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_Unit]:
    return bstream, cl_values.CL_Unit()


def _decode_uref(bstream: bytes, _: cl_types.CL_Type) -> typing.Tuple[bytes, cl_values.CL_URef]:
    assert len(bstream) >= 33
    bstream, encoded = bstream[33:], bstream[0:33]
    access_rights = cl_values.CL_URefAccessRights(encoded[-1])    

    return bstream, cl_values.CL_URef(access_rights, encoded[:-1])


_DECODERS = {
    cl_values.CL_Any: _decode_any,
    cl_values.CL_Bool: _decode_bool,
    cl_values.CL_ByteArray: _decode_byte_array,
    cl_values.CL_I32: _decode_i32,
    cl_values.CL_I64: _decode_i64,
    cl_values.CL_Key: _decode_key,
    cl_values.CL_List: _decode_list,
    cl_values.CL_Option: _decode_option,
    cl_values.CL_Map: _decode_map,
    cl_values.CL_PublicKey: _decode_public_key,
    cl_values.CL_Result: _decode_result,
    cl_values.CL_String: _decode_string,
    cl_values.CL_Tuple1: _decode_tuple_1,
    cl_values.CL_Tuple2: _decode_tuple_2,
    cl_values.CL_Tuple3: _decode_tuple_3,
    cl_values.CL_U8: _decode_u8,
    cl_values.CL_U32: _decode_u32,
    cl_values.CL_U64: _decode_u64,
    cl_values.CL_U128: _decode_u128,
    cl_values.CL_U256: _decode_u256,
    cl_values.CL_U512: _decode_u512,
    cl_values.CL_Unit: _decode_unit,
    cl_values.CL_URef: _decode_uref,
}
