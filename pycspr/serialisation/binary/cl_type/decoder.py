from pycspr.serialisation.binary.cl_value import decode as decode_cl_value
from pycspr.types.cl import CL_Type
from pycspr.types.cl import CL_TypeKey
from pycspr.types.cl import CL_Type_Any
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
from pycspr.types.cl import CL_Type_Result
from pycspr.types.cl import CL_Type_String
from pycspr.types.cl import CL_Type_Tuple1
from pycspr.types.cl import CL_Type_Tuple2
from pycspr.types.cl import CL_Type_Tuple3
from pycspr.types.cl import CL_Type_Unit
from pycspr.types.cl import CL_Type_URef


def decode(bstream: bytes) -> CL_Type:
    """Decoder: CL type info <- an array of bytes.

    :param bstream: An array of bytes being decoded.
    :returns: A CL type definition.

    """
    typekey, bstream = CL_TypeKey(int(bstream[0])), bstream[1:]
    if typekey in _DECODERS["simple"]:        
        return bstream, _DECODERS["simple"][typekey]()
    elif typekey in _DECODERS["complex"]:
        return _DECODERS["complex"][typekey](bstream)
    else:
        raise ValueError("Unsupported cl type tag")


def _decode_byte_array(bstream: bytes):
    bstream, size = decode_cl_value(bstream, CL_Type_U32())

    return bstream, CL_Type_ByteArray(size.value)


def _decode_list(bstream: bytes):
    bstream, item_type = decode(bstream)

    return bstream, CL_Type_List(item_type)


def _decode_map(bstream: bytes):
    bstream, key_type = decode(bstream)
    bstream, value_type = decode(bstream)

    return bstream, CL_Type_Map(key_type, value_type)


def _decode_option(bstream: bytes):
    bstream, option_type = decode(bstream)

    return bstream, CL_Type_Option(option_type)


def _decode_tuple_1(bstream: bytes):
    bstream, t0_type = decode(bstream)

    return bstream, CL_Type_Tuple1(t0_type)


def _decode_tuple_2(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)

    return bstream, CL_Type_Tuple2(t0_type, t1_type)


def _decode_tuple_3(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)
    bstream, t2_type = decode(bstream)

    return bstream, CL_Type_Tuple3(t0_type, t1_type, t2_type)


_DECODERS = {
    "complex": {
        CL_TypeKey.BYTE_ARRAY: _decode_byte_array,
        CL_TypeKey.LIST: _decode_list,
        CL_TypeKey.MAP: _decode_map,
        CL_TypeKey.OPTION: _decode_option,
        CL_TypeKey.TUPLE_1: _decode_tuple_1,
        CL_TypeKey.TUPLE_2: _decode_tuple_2,
        CL_TypeKey.TUPLE_3: _decode_tuple_3,
    },
    "simple": {
        CL_TypeKey.ANY: CL_Type_Any,
        CL_TypeKey.BOOL: CL_Type_Bool,
        CL_TypeKey.I32: CL_Type_I32,
        CL_TypeKey.I64: CL_Type_I64,
        CL_TypeKey.KEY: CL_Type_Key,
        CL_TypeKey.PUBLIC_KEY: CL_Type_PublicKey,
        CL_TypeKey.RESULT: CL_Type_Result,
        CL_TypeKey.STRING: CL_Type_String,
        CL_TypeKey.U8: CL_Type_U8,
        CL_TypeKey.U32: CL_Type_U32,
        CL_TypeKey.U64: CL_Type_U64,
        CL_TypeKey.U128: CL_Type_U128,
        CL_TypeKey.U256: CL_Type_U256,
        CL_TypeKey.U512: CL_Type_U512,
        CL_TypeKey.UNIT: CL_Type_Unit,
        CL_TypeKey.UREF: CL_Type_URef,
    }
}
