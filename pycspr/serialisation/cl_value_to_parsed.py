from pycspr.crypto import cl_checksum
from pycspr.types import cl_values


def encode(entity: cl_values.CL_Value) -> object:
    """Encodes a CL value as value interpretable by humans.

    :param entity: A CL value to be encoded.
    :returns: A humanized CL value representation.
    
    """    
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("CL value cannot be encoded as a human interpretable value")
    else:
        return encoder(entity)


def _encode_any(entity: cl_values.CL_Any) -> object:
    raise NotImplementedError()


def _encode_bool(entity: cl_values.CL_Bool) -> bytes:
    return str(entity.value)


def _encode_byte_array(entity: cl_values.CL_ByteArray) -> bytes:
    return cl_checksum.encode(entity.value)


def _encode_i32(entity: cl_values.CL_I32) -> bytes:
    return entity.value


def _encode_i64(entity: cl_values.CL_I64) -> bytes:
    return entity.value


def _encode_key(entity: cl_values.CL_Key) -> bytes:
    if entity.key_type == cl_values.CL_KeyType.ACCOUNT:
        return {
            "Account": f"account-hash-{cl_checksum.encode(entity.identifier)}"
        }
    elif entity.key_type == cl_values.CL_KeyType.HASH:
        return {
            "Hash": f"hash-{cl_checksum.encode(entity.identifier)}"
        }
    elif entity.key_type == cl_values.CL_KeyType.UREF:
        return {
            "URef": f"uref-{cl_checksum.encode(entity.identifier)}"
        }


def _encode_list(entity: cl_values.CL_List) -> bytes:
    return [encode(i) for i in entity.vector]


def _encode_map(entity: cl_values.CL_Map) -> bytes:
    return [{
        "key": encode(k),
        "value": encode(v),
    } for (k, v) in entity.value]


def _encode_option(entity: cl_values.CL_Option) -> bytes:
    return encode(entity.value) if entity.value is not None else ""


def _encode_public_key(entity: cl_values.CL_PublicKey) -> bytes:
    return cl_checksum.encode_account_key(entity.account_key)


def _encode_result(entity: cl_values.CL_Result) -> bytes:
    raise NotImplementedError()


def _encode_string(entity: cl_values.CL_String) -> bytes:
    return entity.value


def _encode_tuple_1(entity: cl_values.CL_Tuple1) -> bytes:
    return (
        encode(entity.v0),
    )


def _encode_tuple_2(entity: cl_values.CL_Tuple2) -> bytes:
    return (
        encode(entity.v0),
        encode(entity.v1),
    )


def _encode_tuple_3(entity: cl_values.CL_Tuple3) -> bytes:
    return (
        encode(entity.v0),
        encode(entity.v1),
        encode(entity.v2),
    )


def _encode_u8(entity: cl_values.CL_U8) -> bytes:
    return entity.value


def _encode_u32(entity: cl_values.CL_U32) -> bytes:
    return entity.value


def _encode_u64(entity: cl_values.CL_U64) -> bytes:
    return entity.value


def _encode_u128(entity: cl_values.CL_U128) -> bytes:
    return str(entity.value)


def _encode_u256(entity: cl_values.CL_U256) -> bytes:
    return str(entity.value)


def _encode_u512(entity: cl_values.CL_U512) -> bytes:
    return str(entity.value)


def _encode_unit(_: cl_values.CL_Unit) -> bytes:
    return ""


def _encode_uref(entity: cl_values.CL_URef) -> bytes:
    return f"uref-{cl_checksum.encode(entity.address)}-{entity.access_rights.value:03}"


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
