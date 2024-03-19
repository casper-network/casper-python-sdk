from pycspr.types import cl_types
from pycspr.types import cl_values


def encode(entity: cl_values.CL_Value) -> cl_types.CL_Type:
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


def _encode_list(entity: cl_values.CL_List):
    if len(entity.vector) == 0:
        raise ValueError("List is empty, therefore cannot derive it's item cl type")

    i = entity.vector[0]
    for i1 in entity.vector[1:]:
        if type(i) is not type(i1):
            raise ValueError("Inconsistent list item types")

    return cl_types.CL_Type_List(encode(i))


def _encode_map(entity: cl_values.CL_Map):
    if len(entity.value) == 0:
        raise ValueError("Map is empty, therefore cannot derive it's cl type")

    k, v = entity.value[0]
    for k1, v1 in entity.value[1:]:
        if type(k1) is not type(k) or type(v1) is not type(v):
            raise ValueError("Inconsistent value name/key pairs")

    return cl_types.CL_Type_Map(encode(k), encode(v))


_ENCODERS: dict = {
    "complex": {
        cl_values.CL_ByteArray:
            lambda x: cl_types.CL_Type_ByteArray(len(x)),
        cl_values.CL_List:
            _encode_list,
        cl_values.CL_Map:
            _encode_map,
        cl_values.CL_Option:
            lambda x: cl_types.CL_Type_Option(x.option_type),
        cl_values.CL_Tuple1:
            lambda x: cl_types.CL_Type_Tuple1(encode(x.v0)),
        cl_values.CL_Tuple2:
            lambda x: cl_types.CL_Type_Tuple2(encode(x.v0), encode(x.v1)),
        cl_values.CL_Tuple3:
            lambda x: cl_types.CL_Type_Tuple3(encode(x.v0), encode(x.v1), encode(x.v2)),
    },
    "simple": {
        cl_values.CL_Bool: cl_types.CL_Type_Bool,
        cl_values.CL_I32: cl_types.CL_Type_I32,
        cl_values.CL_I64: cl_types.CL_Type_I64,
        cl_values.CL_Key: cl_types.CL_Type_Key,
        cl_values.CL_PublicKey: cl_types.CL_Type_PublicKey,
        cl_values.CL_String: cl_types.CL_Type_String,
        cl_values.CL_U8: cl_types.CL_Type_U8,
        cl_values.CL_U32: cl_types.CL_Type_U32,
        cl_values.CL_U64: cl_types.CL_Type_U64,
        cl_values.CL_U128: cl_types.CL_Type_U128,
        cl_values.CL_U256: cl_types.CL_Type_U256,
        cl_values.CL_U512: cl_types.CL_Type_U512,
        cl_values.CL_Unit: cl_types.CL_Type_Unit,
        cl_values.CL_URef: cl_types.CL_Type_URef,
    }
}
