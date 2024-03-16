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


def _encode_map(entity: cl_values.CL_Map) -> bytes:
    return [{
        "key": encode(k),
        "value": encode(v),
    } for (k, v) in entity.value]


def _encode_result(entity: cl_values.CL_Result) -> bytes:
    raise NotImplementedError()


def _encode_uref(entity: cl_values.CL_URef) -> bytes:
    return f"uref-{cl_checksum.encode(entity.address)}-{entity.access_rights.value:03}"


_ENCODERS = {
    cl_values.CL_Any: _encode_any,
    cl_values.CL_Bool: lambda x: str(x.value),
    cl_values.CL_ByteArray: lambda x: cl_checksum.encode(x.value),
    cl_values.CL_I32: lambda x: x.value,
    cl_values.CL_I64: lambda x: x.value,
    cl_values.CL_Key: _encode_key,
    cl_values.CL_List: lambda x: [encode(i) for i in x.vector],
    cl_values.CL_Map: _encode_map,
    cl_values.CL_Option: lambda x: "" if x.value is None else encode(x.value),
    cl_values.CL_PublicKey: lambda x: cl_checksum.encode_account_key(x.account_key),
    cl_values.CL_Result: _encode_result,
    cl_values.CL_String: lambda x: x.value,
    cl_values.CL_Tuple1: lambda x: (encode(x.v0),),
    cl_values.CL_Tuple2: lambda x: (encode(x.v0), encode(x.v1)),
    cl_values.CL_Tuple3: lambda x: (encode(x.v0), encode(x.v1), encode(x.v2)),
    cl_values.CL_U8: lambda x: x.value,
    cl_values.CL_U32: lambda x: x.value,
    cl_values.CL_U64: lambda x: x.value,
    cl_values.CL_U128: lambda x: str(x.value),
    cl_values.CL_U256: lambda x: str(x.value),
    cl_values.CL_U512: lambda x: str(x.value),  
    cl_values.CL_Unit: lambda x: "",
    cl_values.CL_URef: _encode_uref,
}
