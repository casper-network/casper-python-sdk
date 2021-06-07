from pycspr.serialization import byte_stream
from pycspr.serialization.utils import HexString
from pycspr.serialization.utils import CLType
from pycspr.serialization.utils import DecoderError
from pycspr.serialization.utils import EncoderError



def decode(data: HexString) -> object:
    """Returns domain type instance decoded from a hexidecimal string representation.

    :param data: Domain data encoded as a hexidecimal string.

    :returns: A domain type instance.

    """
    try:
        assert isinstance(data, str) and len(data) > 0
    except AssertionError:
        raise DecoderError(ENCODING, f"Input data cannot be decoded.")

    return byte_stream.decode(bytes.fromhex(data))


def encode(typeof: CLType, value: object) -> HexString:
    """Returns a domain type instance encoded as a byte stream.

    :param typeof: Domain type to which data can be mapped, e.g. BOOL.
    :param value: Domain type instance to be encoded.

    :returns: Domain instance appropriately encoded.

    """   
    return byte_stream.encode(typeof, value).hex()
