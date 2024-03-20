from pycspr.crypto import cl_checksum
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
from pycspr.types.cl import CL_KeyType
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


def encode(entity: CL_Value) -> object:
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


def _encode_any(entity: CL_Any) -> object:
    raise NotImplementedError()


def _encode_key(entity: CL_Key) -> bytes:
    if entity.key_type == CL_KeyType.ACCOUNT:
        return {
            "Account": f"account-hash-{cl_checksum.encode(entity.identifier)}"
        }
    elif entity.key_type == CL_KeyType.HASH:
        return {
            "Hash": f"hash-{cl_checksum.encode(entity.identifier)}"
        }
    elif entity.key_type == CL_KeyType.UREF:
        return {
            "URef": f"uref-{cl_checksum.encode(entity.identifier)}"
        }


def _encode_result(entity: CL_Result) -> bytes:
    raise NotImplementedError()


_ENCODERS = {
    CL_Any:
        _encode_any,
    CL_Bool:
        lambda x: str(x.value),
    CL_ByteArray:
        lambda x: cl_checksum.encode(x.value),
    CL_I32:
        lambda x: x.value,
    CL_I64:
        lambda x: x.value,
    CL_Key:
        _encode_key,
    CL_List:
        lambda x: [encode(i) for i in x.vector],
    CL_Map:
        lambda x: [{"key": encode(k), "value": encode(v)} for (k, v) in x.value],
    CL_Map:
        lambda x: x,
    CL_Option:
        lambda x: "" if x.value is None else encode(x.value),
    CL_PublicKey:
        lambda x: cl_checksum.encode_account_key(x.account_key),
    CL_Result:
        _encode_result,
    CL_String:
        lambda x: x.value,
    CL_Tuple1:
        lambda x: (encode(x.v0),),
    CL_Tuple2:
        lambda x: (encode(x.v0), encode(x.v1)),
    CL_Tuple3:
        lambda x: (encode(x.v0), encode(x.v1), encode(x.v2)),
    CL_U8:
        lambda x: x.value,
    CL_U32:
        lambda x: x.value,
    CL_U64:
        lambda x: x.value,
    CL_U128:
        lambda x: str(x.value),
    CL_U256:
        lambda x: str(x.value),
    CL_U512:
        lambda x: str(x.value),
    CL_Unit:
        lambda x: "",
    CL_URef:
        lambda x: f"uref-{cl_checksum.encode(x.address)}-{x.access_rights.value:03}",
}
