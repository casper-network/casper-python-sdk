from pycspr.serializer.binary.encoder_clv import encode as encode_clv
from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.cl_types import CLT_TypeKey
from pycspr.type_defs.cl_values import CLV_U32


def encode(entity: CLT_Type) -> bytes:
    """Encoder: CL type -> an array of bytes.

    :param entity: A CL type to be encoded.
    :returns: An array of bytes.

    """
    if entity.type_key in _ENCODERS["simple"]:
        return bytes([entity.type_key.value]) + bytes([])
    elif entity.type_key in _ENCODERS["complex"]:
        return \
            bytes([entity.type_key.value]) + \
            _ENCODERS["complex"][entity.type_key](entity)
    else:
        raise ValueError("Unrecognized cl type")


_ENCODERS: dict = {
    "complex": {
        CLT_TypeKey.BYTE_ARRAY: lambda x: encode_clv(CLV_U32(x.size)),
        CLT_TypeKey.LIST: lambda x: encode(x.inner_type),
        CLT_TypeKey.MAP: lambda x: encode(x.key_type) + encode(x.value_type),
        CLT_TypeKey.OPTION: lambda x: encode(x.inner_type),
        CLT_TypeKey.TUPLE_1: lambda x: encode(x.t0_type),
        CLT_TypeKey.TUPLE_2: lambda x: encode(x.t0_type) + encode(x.t1_type),
        CLT_TypeKey.TUPLE_3: lambda x: encode(x.t0_type) + encode(x.t1_type) + encode(x.t2_type),
    },
    "simple": {
        CLT_TypeKey.ANY,
        CLT_TypeKey.BOOL,
        CLT_TypeKey.I32,
        CLT_TypeKey.I64,
        CLT_TypeKey.KEY,
        CLT_TypeKey.PUBLIC_KEY,
        CLT_TypeKey.RESULT,
        CLT_TypeKey.STRING,
        CLT_TypeKey.U8,
        CLT_TypeKey.U32,
        CLT_TypeKey.U64,
        CLT_TypeKey.U128,
        CLT_TypeKey.U256,
        CLT_TypeKey.U512,
        CLT_TypeKey.UNIT,
        CLT_TypeKey.UREF,
    }
}
