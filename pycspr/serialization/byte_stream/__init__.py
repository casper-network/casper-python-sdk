from pycspr.serialization import byte_array
from pycspr.serialization.utils import ByteStream
from pycspr.serialization.utils import CLEncoding
from pycspr.serialization.utils import CLType
from pycspr.serialization.utils import DecoderError
from pycspr.serialization.utils import EncoderError



# Type of encoder.
ENCODING = CLEncoding.BYTE_STREAM


def decode(data: ByteStream) -> object:
    """Returns domain type instance decoded from a byte stream representation.

    :param data: Domain data encoded as a byte stream.

    :returns: A domain type instance.

    """
    try:
        assert isinstance(data, bytes) and len(data) > 0
    except AssertionError:
        raise DecoderError(ENCODING, f"Input data cannot be decoded.")

    return byte_array.decode(list(data))


def encode(typeof: CLType, value: object) -> ByteStream:
    """Returns a domain type instance encoded as a byte stream.

    :param typeof: Domain type to which data can be mapped, e.g. BOOL.
    :param value: Domain type instance to be encoded.

    :returns: Domain instance appropriately encoded.

    """   
    return bytes(byte_array.encode(typeof, value))
