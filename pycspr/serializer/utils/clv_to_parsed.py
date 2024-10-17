from pycspr.crypto import checksummer
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
from pycspr.type_defs.cl_values import CLV_URef


def encode(entity: CLV_Value) -> object:
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


def _encode_any(entity: CLV_Any) -> object:
    raise NotImplementedError()


def _encode_key(entity: CLV_Key) -> bytes:
    if entity.key_type == CLV_KeyType.ACCOUNT:
        return {
            "Account": f"account-hash-{checksummer.encode_bytes(entity.identifier)}"
        }
    elif entity.key_type == CLV_KeyType.HASH:
        return {
            "Hash": f"hash-{checksummer.encode_bytes(entity.identifier)}"
        }
    elif entity.key_type == CLV_KeyType.UREF:
        return {
            "URef": f"uref-{checksummer.encode_bytes(entity.identifier)}"
        }


def _encode_result(entity: CLV_Result) -> bytes:
    raise NotImplementedError()


_ENCODERS = {
    CLV_Any:
        _encode_any,
    CLV_Bool:
        lambda x: str(x.value),
    CLV_ByteArray:
        lambda x: checksummer.encode_bytes(x.value),
    CLV_I32:
        lambda x: x.value,
    CLV_I64:
        lambda x: x.value,
    CLV_Key:
        _encode_key,
    CLV_List:
        lambda x: [encode(i) for i in x.vector],
    CLV_Map:
        lambda x: [{"key": encode(k), "value": encode(v)} for (k, v) in x.value],
    CLV_Option:
        lambda x: "" if x.value is None else encode(x.value),
    CLV_PublicKey:
        lambda x: checksummer.encode_account_key(x.account_key),
    CLV_Result:
        _encode_result,
    CLV_String:
        lambda x: x.value,
    CLV_Tuple1:
        lambda x: (encode(x.v0),),
    CLV_Tuple2:
        lambda x: (encode(x.v0), encode(x.v1)),
    CLV_Tuple3:
        lambda x: (encode(x.v0), encode(x.v1), encode(x.v2)),
    CLV_U8:
        lambda x: x.value,
    CLV_U32:
        lambda x: x.value,
    CLV_U64:
        lambda x: x.value,
    CLV_U128:
        lambda x: str(x.value),
    CLV_U256:
        lambda x: str(x.value),
    CLV_U512:
        lambda x: str(x.value),
    CLV_Unit:
        lambda x: "",
    CLV_URef:
        lambda x: f"uref-{checksummer.encode_bytes(x.address)}-{x.access_rights.value:03}",
}
