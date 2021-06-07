from pycspr.serialization.byte_array import cl_boolean
from pycspr.serialization.byte_array import cl_i32
from pycspr.serialization.byte_array import cl_i64
from pycspr.serialization.byte_array import cl_string
from pycspr.serialization.byte_array import cl_u8
from pycspr.serialization.byte_array import cl_u32
from pycspr.serialization.byte_array import cl_u64
from pycspr.serialization.byte_array import cl_u128
from pycspr.serialization.byte_array import cl_u256
from pycspr.serialization.byte_array import cl_u512
from pycspr.serialization.byte_array import cl_unit
from pycspr.serialization.utils import ByteArray
from pycspr.serialization.utils import CLEncoding
from pycspr.serialization.utils import CLType
from pycspr.serialization.utils import DecoderError
from pycspr.serialization.utils import EncoderError


# Type of encoder.
ENCODING = CLEncoding.BYTE_ARRAY

# Map: CL type <-> codec.
CODECS = {
    CLType.BOOL: cl_boolean,
    CLType.I32: cl_i32,
    CLType.I64: cl_i64,    
    CLType.STRING: cl_string,
    CLType.U8: cl_u8,
    CLType.U32: cl_u32,
    CLType.U64: cl_u64,
    CLType.U128: cl_u128,
    CLType.U256: cl_u256,
    CLType.U512: cl_u512,
    CLType.UNIT: cl_unit,
}

# Set of supported type prefixes.
TYPE_TAGS = set([i.value for i in list(CLType)])


def decode(data: ByteArray) -> object:
    """Returns domain type instance decoded from a previously encoded instance.

    :param data: Domain data appropriately encoded.

    :returns: Domain type instance.

    """
    # Verify data is decodeable - 1.
    try:
        assert isinstance(data, list) and len(data) > 0
    except AssertionError:
        raise DecoderError(ENCODING, f"Input data cannot be decoded.")

    # Destructure type tag and byte array from input data.
    tag, data = data[0], data[1:]

    # Map type tag -> CL type.
    try:
        typeof = CLType(tag)
    except ValueError:
        raise DecoderError(ENCODING, f"Input data cannot be decoded.")    

    # Map CL type -> codec.
    try:
        codec = CODECS[typeof]
    except KeyError:
        raise DecoderError(ENCODING, f"{typeof} decoder unsupported")    

    # Verify data is decodeable - 2.
    try:
        assert codec.is_decodeable(data)
    except AssertionError:
        raise DecoderError(ENCODING, f"{typeof} {data} decoding unfeasible")    

    return codec.decode(data)


def encode(typeof: CLType, value: object) -> ByteArray:
    """Returns a domain type instance encoded as a byte array.

    :param typeof: Domain type to which data can be mapped, e.g. BOOL.
    :param value: Domain type instance to be encoded.

    :returns: Domain instance appropriately encoded.

    """    
    try:
        codec = CODECS[typeof]
    except KeyError:
        raise EncoderError(ENCODING, f"{typeof} encoder unsupported")

    try:
        assert codec.is_encodeable(value)
    except AssertionError:
        raise EncoderError(ENCODING, f"{typeof} -- {value} encoding unfeasible")    

    return [typeof.value] + codec.encode(value)
