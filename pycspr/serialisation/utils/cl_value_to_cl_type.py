from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLT_Type_Bool
from pycspr.types.cl import CLT_Type_ByteArray
from pycspr.types.cl import CLT_Type_I32
from pycspr.types.cl import CLT_Type_I64
from pycspr.types.cl import CLT_Type_U8
from pycspr.types.cl import CLT_Type_U32
from pycspr.types.cl import CLT_Type_U64
from pycspr.types.cl import CLT_Type_U128
from pycspr.types.cl import CLT_Type_U256
from pycspr.types.cl import CLT_Type_U512
from pycspr.types.cl import CLT_Type_Key
from pycspr.types.cl import CLT_Type_List
from pycspr.types.cl import CLT_Type_Map
from pycspr.types.cl import CLT_Type_Option
from pycspr.types.cl import CLT_Type_PublicKey
from pycspr.types.cl import CLT_Type_String
from pycspr.types.cl import CLT_Type_Tuple1
from pycspr.types.cl import CLT_Type_Tuple2
from pycspr.types.cl import CLT_Type_Tuple3
from pycspr.types.cl import CLT_Type_Unit
from pycspr.types.cl import CLT_Type_URef
from pycspr.types.cl import CLV_Value
from pycspr.types.cl import CLV_Bool
from pycspr.types.cl import CLV_ByteArray
from pycspr.types.cl import CLV_I32
from pycspr.types.cl import CLV_I64
from pycspr.types.cl import CLV_U8
from pycspr.types.cl import CLV_U32
from pycspr.types.cl import CLV_U64
from pycspr.types.cl import CLV_U128
from pycspr.types.cl import CLV_U256
from pycspr.types.cl import CLV_U512
from pycspr.types.cl import CLV_Key
from pycspr.types.cl import CLV_List
from pycspr.types.cl import CLV_Map
from pycspr.types.cl import CLV_Option
from pycspr.types.cl import CLV_PublicKey
from pycspr.types.cl import CLV_String
from pycspr.types.cl import CLV_Tuple1
from pycspr.types.cl import CLV_Tuple2
from pycspr.types.cl import CLV_Tuple3
from pycspr.types.cl import CLV_Unit
from pycspr.types.cl import CLV_URef


def encode(entity: CLV_Value) -> CLT_Type:
    """Encodes a CL value as a CL type definition.

    :param entity: A CL value to be encoded.
    :returns: A CL type definition.

    """
    typedef = type(entity)
    if typedef in _ENCODERS["complex"]:
        return _ENCODERS["complex"][typedef](entity)
    elif typedef in _ENCODERS["simple"]:
        return _ENCODERS["simple"][typedef]()
    else:
        raise NotImplementedError(f"CL value cannot be encoded as CL type: {typedef}")


def _encode_list(entity: CLV_List):
    if len(entity.vector) == 0:
        raise ValueError("List is empty, therefore cannot derive it's item cl type")

    i = entity.vector[0]
    for i1 in entity.vector[1:]:
        if type(i) is not type(i1):
            raise ValueError("Inconsistent list item types")

    return CLT_Type_List(encode(i))


def _encode_map(entity: CLV_Map):
    if len(entity.value) == 0:
        raise ValueError("Map is empty, therefore cannot derive it's cl type")

    k, v = entity.value[0]
    for k1, v1 in entity.value[1:]:
        if type(k1) is not type(k) or type(v1) is not type(v):
            raise ValueError("Inconsistent value name/key pairs")

    return CLT_Type_Map(encode(k), encode(v))


_ENCODERS: dict = {
    "complex": {
        CLV_ByteArray:
            lambda x: CLT_Type_ByteArray(len(x)),
        CLV_List:
            _encode_list,
        CLV_Map:
            _encode_map,
        CLV_Option:
            lambda x: CLT_Type_Option(x.option_type),
        CLV_Tuple1:
            lambda x: CLT_Type_Tuple1(encode(x.v0)),
        CLV_Tuple2:
            lambda x: CLT_Type_Tuple2(encode(x.v0), encode(x.v1)),
        CLV_Tuple3:
            lambda x: CLT_Type_Tuple3(encode(x.v0), encode(x.v1), encode(x.v2)),
    },
    "simple": {
        CLV_Bool: CLT_Type_Bool,
        CLV_I32: CLT_Type_I32,
        CLV_I64: CLT_Type_I64,
        CLV_Key: CLT_Type_Key,
        CLV_PublicKey: CLT_Type_PublicKey,
        CLV_String: CLT_Type_String,
        CLV_U8: CLT_Type_U8,
        CLV_U32: CLT_Type_U32,
        CLV_U64: CLT_Type_U64,
        CLV_U128: CLT_Type_U128,
        CLV_U256: CLT_Type_U256,
        CLV_U512: CLT_Type_U512,
        CLV_Unit: CLT_Type_Unit,
        CLV_URef: CLT_Type_URef,
    }
}
