from pycspr.types.cl import CL_Type
from pycspr.types.cl import CL_Type_Bool
from pycspr.types.cl import CL_Type_ByteArray
from pycspr.types.cl import CL_Type_I32
from pycspr.types.cl import CL_Type_I64
from pycspr.types.cl import CL_Type_U8
from pycspr.types.cl import CL_Type_U32
from pycspr.types.cl import CL_Type_U64
from pycspr.types.cl import CL_Type_U128
from pycspr.types.cl import CL_Type_U256
from pycspr.types.cl import CL_Type_U512
from pycspr.types.cl import CL_Type_Key
from pycspr.types.cl import CL_Type_List
from pycspr.types.cl import CL_Type_Map
from pycspr.types.cl import CL_Type_Option
from pycspr.types.cl import CL_Type_PublicKey
from pycspr.types.cl import CL_Type_String
from pycspr.types.cl import CL_Type_Tuple1
from pycspr.types.cl import CL_Type_Tuple2
from pycspr.types.cl import CL_Type_Tuple3
from pycspr.types.cl import CL_Type_Unit
from pycspr.types.cl import CL_Type_URef
from pycspr.types.cl import CL_Value
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
from pycspr.types.cl import CL_List
from pycspr.types.cl import CL_Map
from pycspr.types.cl import CL_Option
from pycspr.types.cl import CL_PublicKey
from pycspr.types.cl import CL_String
from pycspr.types.cl import CL_Tuple1
from pycspr.types.cl import CL_Tuple2
from pycspr.types.cl import CL_Tuple3
from pycspr.types.cl import CL_Unit
from pycspr.types.cl import CL_URef


def encode(entity: CL_Value) -> CL_Type:
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


def _encode_list(entity: CL_List):
    if len(entity.vector) == 0:
        raise ValueError("List is empty, therefore cannot derive it's item cl type")

    i = entity.vector[0]
    for i1 in entity.vector[1:]:
        if type(i) is not type(i1):
            raise ValueError("Inconsistent list item types")

    return CL_Type_List(encode(i))


def _encode_map(entity: CL_Map):
    if len(entity.value) == 0:
        raise ValueError("Map is empty, therefore cannot derive it's cl type")

    k, v = entity.value[0]
    for k1, v1 in entity.value[1:]:
        if type(k1) is not type(k) or type(v1) is not type(v):
            raise ValueError("Inconsistent value name/key pairs")

    return CL_Type_Map(encode(k), encode(v))


_ENCODERS: dict = {
    "complex": {
        CL_ByteArray:
            lambda x: CL_Type_ByteArray(len(x)),
        CL_List:
            _encode_list,
        CL_Map:
            _encode_map,
        CL_Option:
            lambda x: CL_Type_Option(x.option_type),
        CL_Tuple1:
            lambda x: CL_Type_Tuple1(encode(x.v0)),
        CL_Tuple2:
            lambda x: CL_Type_Tuple2(encode(x.v0), encode(x.v1)),
        CL_Tuple3:
            lambda x: CL_Type_Tuple3(encode(x.v0), encode(x.v1), encode(x.v2)),
    },
    "simple": {
        CL_Bool: CL_Type_Bool,
        CL_I32: CL_Type_I32,
        CL_I64: CL_Type_I64,
        CL_Key: CL_Type_Key,
        CL_PublicKey: CL_Type_PublicKey,
        CL_String: CL_Type_String,
        CL_U8: CL_Type_U8,
        CL_U32: CL_Type_U32,
        CL_U64: CL_Type_U64,
        CL_U128: CL_Type_U128,
        CL_U256: CL_Type_U256,
        CL_U512: CL_Type_U512,
        CL_Unit: CL_Type_Unit,
        CL_URef: CL_Type_URef,
    }
}
