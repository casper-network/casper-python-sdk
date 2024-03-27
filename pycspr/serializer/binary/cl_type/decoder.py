from pycspr.serializer.binary.cl_value import decode as decode_cl_value
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLT_TypeKey
from pycspr.types.cl import CLT_Type_Any
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
from pycspr.types.cl import CLT_Type_Result
from pycspr.types.cl import CLT_Type_String
from pycspr.types.cl import CLT_Type_Tuple1
from pycspr.types.cl import CLT_Type_Tuple2
from pycspr.types.cl import CLT_Type_Tuple3
from pycspr.types.cl import CLT_Type_Unit
from pycspr.types.cl import CLT_Type_URef


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
    bstream, size = decode_cl_value(bstream, CLT_Type_U32())

    return bstream, CLT_Type_ByteArray(size.value)


def _decode_list(bstream: bytes):
    bstream, item_type = decode(bstream)

    return bstream, CLT_Type_List(item_type)


def _decode_map(bstream: bytes):
    bstream, key_type = decode(bstream)
    bstream, value_type = decode(bstream)

    return bstream, CLT_Type_Map(key_type, value_type)


def _decode_option(bstream: bytes):
    bstream, option_type = decode(bstream)

    return bstream, CLT_Type_Option(option_type)


def _decode_tuple_1(bstream: bytes):
    bstream, t0_type = decode(bstream)

    return bstream, CLT_Type_Tuple1(t0_type)


def _decode_tuple_2(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)

    return bstream, CLT_Type_Tuple2(t0_type, t1_type)


def _decode_tuple_3(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)
    bstream, t2_type = decode(bstream)

    return bstream, CLT_Type_Tuple3(t0_type, t1_type, t2_type)


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
        CLT_TypeKey.ANY: CLT_Type_Any,
        CLT_TypeKey.BOOL: CLT_Type_Bool,
        CLT_TypeKey.I32: CLT_Type_I32,
        CLT_TypeKey.I64: CLT_Type_I64,
        CLT_TypeKey.KEY: CLT_Type_Key,
        CLT_TypeKey.PUBLIC_KEY: CLT_Type_PublicKey,
        CLT_TypeKey.RESULT: CLT_Type_Result,
        CLT_TypeKey.STRING: CLT_Type_String,
        CLT_TypeKey.U8: CLT_Type_U8,
        CLT_TypeKey.U32: CLT_Type_U32,
        CLT_TypeKey.U64: CLT_Type_U64,
        CLT_TypeKey.U128: CLT_Type_U128,
        CLT_TypeKey.U256: CLT_Type_U256,
        CLT_TypeKey.U512: CLT_Type_U512,
        CLT_TypeKey.UNIT: CLT_Type_Unit,
        CLT_TypeKey.UREF: CLT_Type_URef,
    }
}
