from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes
from pycspr.types import cl_types
from pycspr.types import CL_TypeKey


def decode(bstream: bytes) -> cl_types.CL_Type:
    """Decodes a CL type from a byte array.

    :param bstream: An array of bytes being decoded.
    :returns: A CL type definition.

    """
    typekey, bstream = CL_TypeKey(int(bstream[0])), bstream[1:]
    try:
        decoder = _DECODERS_SIMPLE[typekey]
    except KeyError:
        try:
            decoder = _DECODERS_COMPLEX[typekey]
        except KeyError:
            raise ValueError("Unsupported cl type tag")
        else:
            return decoder(bstream)
    else:
        return bstream, decoder()


def _decode_byte_array(bstream: bytes):
    bstream, size = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())

    return bstream, cl_types.CL_Type_ByteArray(size.value)


def _decode_list(bstream: bytes):
    bstream, item_type = decode(bstream)

    return bstream, cl_types.CL_Type_List(item_type)


def _decode_map(bstream: bytes):
    bstream, key_type = decode(bstream)
    bstream, value_type = decode(bstream)

    return bstream, cl_types.CL_Type_Map(key_type, value_type)


def _decode_option(bstream: bytes):
    bstream, option_type = decode(bstream)

    return bstream, cl_types.CL_Type_Option(option_type)


def _decode_tuple_1(bstream: bytes):
    bstream, t0_type = decode(bstream)

    return bstream, cl_types.CL_Type_Tuple1(t0_type)


def _decode_tuple_2(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)

    return bstream, cl_types.CL_Type_Tuple2(t0_type, t1_type)


def _decode_tuple_3(bstream: bytes):
    bstream, t0_type = decode(bstream)
    bstream, t1_type = decode(bstream)
    bstream, t2_type = decode(bstream)

    return bstream, cl_types.CL_Type_Tuple3(t0_type, t1_type, t2_type)


_DECODERS_COMPLEX = {
    CL_TypeKey.BYTE_ARRAY: _decode_byte_array,
    CL_TypeKey.LIST: _decode_list,
    CL_TypeKey.MAP: _decode_map,
    CL_TypeKey.OPTION: _decode_option,
    CL_TypeKey.TUPLE_1: _decode_tuple_1,
    CL_TypeKey.TUPLE_2: _decode_tuple_2,
    CL_TypeKey.TUPLE_3: _decode_tuple_3,
}

_DECODERS_SIMPLE = {
    CL_TypeKey.ANY: cl_types.CL_Type_Any,
    CL_TypeKey.BOOL: cl_types.CL_Type_Bool,
    CL_TypeKey.I32: cl_types.CL_Type_I32,
    CL_TypeKey.I64: cl_types.CL_Type_I64,
    CL_TypeKey.KEY: cl_types.CL_Type_Key,
    CL_TypeKey.PUBLIC_KEY: cl_types.CL_Type_PublicKey,
    CL_TypeKey.RESULT: cl_types.CL_Type_Result,
    CL_TypeKey.STRING: cl_types.CL_Type_String,
    CL_TypeKey.U8: cl_types.CL_Type_U8,
    CL_TypeKey.U32: cl_types.CL_Type_U32,
    CL_TypeKey.U64: cl_types.CL_Type_U64,
    CL_TypeKey.U128: cl_types.CL_Type_U128,
    CL_TypeKey.U256: cl_types.CL_Type_U256,
    CL_TypeKey.U512: cl_types.CL_Type_U512,
    CL_TypeKey.UNIT: cl_types.CL_Type_Unit,
    CL_TypeKey.UREF: cl_types.CL_Type_URef,
}
