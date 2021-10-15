import pycspr.serialisation.byte_array.encoder.cl_complex as complex_encoder
import pycspr.serialisation.byte_array.encoder.cl_primitive as primitives_encoder
import pycspr.serialisation.byte_array.encoder.cl_type as type_encoder
from pycspr.types import CLTypeKey
from pycspr.types import CLValue


# Map: CL type <-> encoder.
ENCODERS = {
    CLTypeKey.ANY: complex_encoder.encode_any,
    CLTypeKey.BOOL: primitives_encoder.encode_bool,
    CLTypeKey.BYTE_ARRAY: primitives_encoder.encode_byte_array,
    CLTypeKey.I32: primitives_encoder.encode_i32,
    CLTypeKey.I64: primitives_encoder.encode_i64,
    CLTypeKey.KEY: complex_encoder.encode_storage_key,
    CLTypeKey.LIST: complex_encoder.encode_list,
    CLTypeKey.MAP: complex_encoder.encode_map,
    CLTypeKey.OPTION: complex_encoder.encode_option,
    CLTypeKey.PUBLIC_KEY: complex_encoder.encode_public_key,
    CLTypeKey.STRING: primitives_encoder.encode_string,
    CLTypeKey.TUPLE_1: complex_encoder.encode_tuple1,
    CLTypeKey.TUPLE_2: complex_encoder.encode_tuple2,
    CLTypeKey.TUPLE_3: complex_encoder.encode_tuple3,
    CLTypeKey.U8: primitives_encoder.encode_u8,
    CLTypeKey.U32: primitives_encoder.encode_u32,
    CLTypeKey.U64: primitives_encoder.encode_u64,
    CLTypeKey.U128: primitives_encoder.encode_u128,
    CLTypeKey.U256: primitives_encoder.encode_u256,
    CLTypeKey.U512: primitives_encoder.encode_u512,
    CLTypeKey.UNIT: primitives_encoder.encode_unit,
    CLTypeKey.RESULT: complex_encoder.encode_result,
    CLTypeKey.UREF: complex_encoder.encode_uref,
}


def encode(value: CLValue) -> bytes:
    """Encodes a CL value as an array of bytes.

    :param value: A CL value that encapsulates both CL type & it's pythonic value representation.
    :returns: A byte array representation conformant to CL serialisation protocol.

    """
    encoder = ENCODERS[value.cl_type.type_key]
    if value.cl_type.type_key in {CLTypeKey.LIST, CLTypeKey.OPTION}:
        return encoder(value.parsed, ENCODERS[value.cl_type.inner_type.type_key])
    elif value.cl_type.type_key == CLTypeKey.KEY:
        return encoder(value.parsed, value.cl_type.key_type)
    else:
        return encoder(value.parsed)


def encode_cl_value(entity: CLValue) -> bytes:
    """Encodes a CL value.

    """
    return \
        primitives_encoder.encode_u8_array(encode(entity)) + \
        type_encoder.encode_cl_type(entity.cl_type)
