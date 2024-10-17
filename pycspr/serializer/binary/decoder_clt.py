from pycspr.serializer.binary.decoder_clv import decode as decode_clv
from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.cl_types import CLT_TypeKey
from pycspr.type_defs.cl_types import CLT_Any
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
from pycspr.type_defs.cl_types import CLT_Result
from pycspr.type_defs.cl_types import CLT_String
from pycspr.type_defs.cl_types import CLT_Tuple1
from pycspr.type_defs.cl_types import CLT_Tuple2
from pycspr.type_defs.cl_types import CLT_Tuple3
from pycspr.type_defs.cl_types import CLT_Unit
from pycspr.type_defs.cl_types import CLT_URef


def decode(bstream: bytes) -> CLT_Type:
    """Decoder: CL type info <- an array of bytes.

    :param bstream: An array of bytes being decoded.
    :returns: A CL type definition.

    """
    typekey, bstream = CLT_TypeKey(int(bstream[0])), bstream[1:]
    if typekey in _DECODERS["simple"]:
        return bstream, _DECODERS["simple"][typekey]()
    elif typekey in _DECODERS["complex"]:
        return _DECODERS["complex"][typekey](bstream)
    else:
        raise ValueError("Unsupported cl type tag")


def _decode_byte_array(bstream: bytes):
    bstream, size = decode_clv(CLT_U32(), bstream)

    return bstream, CLT_ByteArray(size.value)


def _decode_list(bstream: bytes):
    bstream, item_type = decode(bstream)

    return bstream, CLT_List(item_type)


def _decode_map(bstream: bytes):
    bstream, key_type = decode(bstream)
    bstream, value_type = decode(bstream)

    return bstream, CLT_Map(key_type, value_type)


def _decode_option(bstream: bytes):
    bstream, option_type = decode(bstream)

    return bstream, CLT_Option(option_type)


def _decode_tuple_1(bstream: bytes):
    bstream, t0_type = decode(bstream)

    return bstream, CLT_Tuple1(t0_type)


def _decode_tuple_2(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)

    return bstream, CLT_Tuple2(t0_type, t1_type)


def _decode_tuple_3(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)
    bstream, t2_type = decode(bstream)

    return bstream, CLT_Tuple3(t0_type, t1_type, t2_type)


_DECODERS = {
    "complex": {
        CLT_TypeKey.BYTE_ARRAY: _decode_byte_array,
        CLT_TypeKey.LIST: _decode_list,
        CLT_TypeKey.MAP: _decode_map,
        CLT_TypeKey.OPTION: _decode_option,
        CLT_TypeKey.TUPLE_1: _decode_tuple_1,
        CLT_TypeKey.TUPLE_2: _decode_tuple_2,
        CLT_TypeKey.TUPLE_3: _decode_tuple_3,
    },
    "simple": {
        CLT_TypeKey.ANY: CLT_Any,
        CLT_TypeKey.BOOL: CLT_Bool,
        CLT_TypeKey.I32: CLT_I32,
        CLT_TypeKey.I64: CLT_I64,
        CLT_TypeKey.KEY: CLT_Key,
        CLT_TypeKey.PUBLIC_KEY: CLT_PublicKey,
        CLT_TypeKey.RESULT: CLT_Result,
        CLT_TypeKey.STRING: CLT_String,
        CLT_TypeKey.U8: CLT_U8,
        CLT_TypeKey.U32: CLT_U32,
        CLT_TypeKey.U64: CLT_U64,
        CLT_TypeKey.U128: CLT_U128,
        CLT_TypeKey.U256: CLT_U256,
        CLT_TypeKey.U512: CLT_U512,
        CLT_TypeKey.UNIT: CLT_Unit,
        CLT_TypeKey.UREF: CLT_URef,
    }
}
