from pycspr.crypto import cl_checksum
from pycspr.types import cl_values


def encode(entity: cl_values.CL_Value) -> object:
    if isinstance(entity, cl_values.CL_Any):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Bool):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_ByteArray):
        return cl_checksum.encode(entity.value)

    elif isinstance(entity, cl_values.CL_I32):
        return entity.value

    elif isinstance(entity, cl_values.CL_I64):
        return entity.value

    elif isinstance(entity, cl_values.CL_Key):
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

    elif isinstance(entity, cl_values.CL_List):
        return [encode(i) for i in entity.vector]

    elif isinstance(entity, cl_values.CL_Map):
        return [{
            "key": encode(k),
            "value": encode(v),
        } for (k, v) in entity.value]

    elif isinstance(entity, cl_values.CL_PublicKey):
        return cl_checksum.encode_account_key(entity.account_key)

    elif isinstance(entity, cl_values.CL_Result):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_String):
        return entity.value

    elif isinstance(entity, cl_values.CL_Tuple1):
        return (
            encode(entity.v0),
        )
            
    elif isinstance(entity, cl_values.CL_Tuple2):
        return (
            encode(entity.v0),
            encode(entity.v1),
        )

    elif isinstance(entity, cl_values.CL_Tuple3):
        return (
            encode(entity.v0),
            encode(entity.v1),
            encode(entity.v2),
        )

    elif isinstance(entity, cl_values.CL_U8):
        return entity.value

    elif isinstance(entity, cl_values.CL_U32):
        return entity.value

    elif isinstance(entity, cl_values.CL_U64):
        return entity.value

    elif isinstance(entity, cl_values.CL_U128):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_U256):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_U512):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_Unit):
        return ""

    elif isinstance(entity, cl_values.CL_URef):
        return f"uref-{cl_checksum.encode(entity.address)}-{entity.access_rights.value:03}"
