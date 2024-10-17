from pycspr.type_defs.cl_types import CLT_Type
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
from pycspr.type_defs.cl_types import CLT_String
from pycspr.type_defs.cl_types import CLT_Tuple1
from pycspr.type_defs.cl_types import CLT_Tuple2
from pycspr.type_defs.cl_types import CLT_Tuple3
from pycspr.type_defs.cl_types import CLT_Unit
from pycspr.type_defs.cl_types import CLT_URef
from pycspr.type_defs.cl_values import CLV_Value
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
from pycspr.type_defs.cl_values import CLV_List
from pycspr.type_defs.cl_values import CLV_Map
from pycspr.type_defs.cl_values import CLV_Option
from pycspr.type_defs.cl_values import CLV_PublicKey
from pycspr.type_defs.cl_values import CLV_String
from pycspr.type_defs.cl_values import CLV_Tuple1
from pycspr.type_defs.cl_values import CLV_Tuple2
from pycspr.type_defs.cl_values import CLV_Tuple3
from pycspr.type_defs.cl_values import CLV_Unit
from pycspr.type_defs.cl_values import CLV_URef


def encode(entity: CLV_Value) -> CLT_Type:
    """Encodes a CL value as a CL type definition.

    :param entity: A CL value to be encoded.
    :returns: A CL type definition.

    """
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"CL value cannot be encoded as CL type: {type(entity)}")
    else:
        return encoder(entity)


def _encode_list(entity: CLV_List):
    if len(entity.vector) == 0:
        raise ValueError("List is empty, therefore cannot derive it's item cl type")

    i = entity.vector[0]
    for i1 in entity.vector[1:]:
        if type(i) is not type(i1):
            raise ValueError("Inconsistent list item types")

    return CLT_List(encode(i))


def _encode_map(entity: CLV_Map):
    if len(entity.value) == 0:
        raise ValueError("Map is empty, therefore cannot derive it's cl type")

    k, v = entity.value[0]
    for k1, v1 in entity.value[1:]:
        if type(k1) is not type(k) or type(v1) is not type(v):
            raise ValueError("Inconsistent value name/key pairs")

    return CLT_Map(encode(k), encode(v))


_ENCODERS: dict = {
    CLV_Bool:
        lambda _: CLT_Bool(),
    CLV_ByteArray:
        lambda x: CLT_ByteArray(len(x)),
    CLV_I32:
        lambda _: CLT_I32(),
    CLV_I64:
        lambda _: CLT_I64(),
    CLV_Key:
        lambda _: CLT_Key(),
    CLV_List:
        _encode_list,
    CLV_Map:
        _encode_map,
    CLV_Option:
        lambda x: CLT_Option(x.option_type),
    CLV_PublicKey:
        lambda _: CLT_PublicKey(),
    CLV_String:
        lambda _: CLT_String(),
    CLV_Tuple1:
        lambda x: CLT_Tuple1(encode(x.v0)),
    CLV_Tuple2:
        lambda x: CLT_Tuple2(encode(x.v0), encode(x.v1)),
    CLV_Tuple3:
        lambda x: CLT_Tuple3(encode(x.v0), encode(x.v1), encode(x.v2)),
    CLV_U8:
        lambda _: CLT_U8(),
    CLV_U32:
        lambda _: CLT_U32(),
    CLV_U64:
        lambda _: CLT_U64(),
    CLV_U128:
        lambda _: CLT_U128(),
    CLV_U256:
        lambda _: CLT_U256(),
    CLV_U512:
        lambda _: CLT_U512(),
    CLV_Unit:
        lambda _: CLT_Unit(),
    CLV_URef:
        lambda _: CLT_URef(),
}
