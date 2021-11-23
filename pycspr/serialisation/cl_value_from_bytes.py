from pycspr import crypto
from pycspr.types import CL_TYPEKEY_TO_CL_VALUE_TYPE
from pycspr.types.cl import cl_types
from pycspr.types.cl import cl_values
from pycspr.utils.conversion import le_bytes_to_int


def decode(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Value:
    cl_value_type: cl_values.CL_Value = CL_TYPEKEY_TO_CL_VALUE_TYPE[cl_type.type_key]
    try:
        decoder = _DECODERS[cl_value_type]
    except KeyError:
        raise ValueError(f"Unsupported CL value type: {cl_value_type}")
    else:
        return decoder(encoded, cl_type)


def _decode_any(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Any:
    raise NotImplementedError()


def _decode_bool(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_Bool:
    return cl_values.CL_Bool(bool(encoded[0]))


def _decode_byte_array(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_ByteArray:
    return cl_values.CL_ByteArray(encoded)


def _decode_i32(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_I32:
    return cl_values.CL_I32(le_bytes_to_int(encoded, True))


def _decode_i64(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_I64:
    return cl_values.CL_I64(le_bytes_to_int(encoded, True))


def _decode_key(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_Key:
    return cl_values.CL_Key(encoded[1:], cl_values.CL_KeyType(encoded[0]))


def _decode_list(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_List:
    raise NotImplementedError()


def _decode_map(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Map:
    raise NotImplementedError()


def _decode_option(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Option:
    decoded = decode(encoded[1:], cl_type.inner_type) if bool(encoded[0]) else None
    return cl_values.CL_Option(decoded, cl_type.inner_type)


def _decode_public_key(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_PublicKey:
    return cl_values.CL_PublicKey(crypto.KeyAlgorithm(encoded[0]), encoded[1:])


def _decode_result(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Result:
    raise NotImplementedError()


def _decode_string(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_String:
    return cl_values.CL_String(encoded[4:].decode("utf-8"))


def _decode_tuple_1(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Tuple1:
    raise NotImplementedError()


def _decode_tuple_2(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Tuple2:
    raise NotImplementedError()


def _decode_tuple_3(encoded: bytes, cl_type: cl_types.CL_Type) -> cl_values.CL_Tuple3:
    raise NotImplementedError()


def _decode_u8(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_U8:
    return cl_values.CL_U8(le_bytes_to_int(encoded, False))


def _decode_u32(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_U32:
    return cl_values.CL_U32(le_bytes_to_int(encoded, False))


def _decode_u64(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_U64:
    return cl_values.CL_U64(le_bytes_to_int(encoded, False))


def _decode_u128(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_U128:
    return cl_values.CL_U128(le_bytes_to_int(encoded[1:], False))


def _decode_u256(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_U256:
    return cl_values.CL_U256(le_bytes_to_int(encoded[1:], False))


def _decode_u512(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_U512:
    return cl_values.CL_U512(le_bytes_to_int(encoded[1:], False))


def _decode_unit(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_Unit:
    return cl_values.CL_Unit()


def _decode_uref(encoded: bytes, _: cl_types.CL_Type) -> cl_values.CL_URef:
    return cl_values.CL_URef(cl_values.CL_URefAccessRights(encoded[-1]), encoded[:-1])


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
