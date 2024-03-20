from pycspr.serialisation.binary.cl_value import encode as encode_cl_value
from pycspr.types.cl import CL_Type
from pycspr.types.cl import CL_TypeKey
from pycspr.types.cl import CLV_U32


def encode(entity: CL_Type) -> bytes:
    """Encoder: CL type -> an array of bytes.

    :param entity: A CL type to be encoded.
    :returns: An array of bytes.

    """
    if entity.type_key in _ENCODERS["simple"]:
        return bytes([entity.type_key.value]) + bytes([])
    elif entity.type_key in _ENCODERS["complex"]:
        return bytes([entity.type_key.value]) + _ENCODERS["complex"][entity.type_key](entity)
    else:
        raise ValueError("Unrecognized cl type")


_ENCODERS: dict = {
    "complex": {
        CL_TypeKey.BYTE_ARRAY: lambda x: encode_cl_value(CLV_U32(x.size)),
        CL_TypeKey.LIST: lambda x: encode(x.inner_type),
        CL_TypeKey.MAP: lambda x: encode(x.key_type) + encode(x.value_type),
        CL_TypeKey.OPTION: lambda x: encode(x.inner_type),
        CL_TypeKey.TUPLE_1: lambda x: encode(x.t0_type),
        CL_TypeKey.TUPLE_2: lambda x: encode(x.t0_type) + encode(x.t1_type),
        CL_TypeKey.TUPLE_3: lambda x: encode(x.t0_type) + encode(x.t1_type) + encode(x.t2_type),
    },
    "simple": {
        CL_TypeKey.ANY,
        CL_TypeKey.BOOL,
        CL_TypeKey.I32,
        CL_TypeKey.I64,
        CL_TypeKey.KEY,
        CL_TypeKey.PUBLIC_KEY,
        CL_TypeKey.RESULT,
        CL_TypeKey.STRING,
        CL_TypeKey.U8,
        CL_TypeKey.U32,
        CL_TypeKey.U64,
        CL_TypeKey.U128,
        CL_TypeKey.U256,
        CL_TypeKey.U512,
        CL_TypeKey.UNIT,
        CL_TypeKey.UREF,
    }
}
