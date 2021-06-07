import typing

from pycspr.serialization import byte_array
from pycspr.serialization import byte_stream
from pycspr.serialization import hex_string
from pycspr.serialization.utils import ByteArray
from pycspr.serialization.utils import CLType
from pycspr.serialization.utils import ByteStream
from pycspr.serialization.utils import CLEncoding
from pycspr.serialization.utils import CLType
from pycspr.serialization.utils import DecoderError
from pycspr.serialization.utils import EncoderError
from pycspr.serialization.utils import HexString



# Map: CL encoding <-> codec.
CODECS = {
    CLEncoding.BYTE_ARRAY: byte_array,
    CLEncoding.BYTE_STREAM: byte_stream,
    CLEncoding.HEX_STRING: hex_string,
}


def decode(data: typing.Union[ByteArray, ByteStream, HexString], encoding: CLEncoding = CLEncoding.BYTE_STREAM) -> object:
    """Returns domain type instance decoded from a previously encoded instance.

    :param data: Domain data appropriately encoded.
    :param encoding: A supported encoding.

    :returns: Domain type instance.

    """
    try:
        codec = CODECS[encoding]
    except KeyError:
        raise DecoderError(encoding, "Unsupported encoding.")    

    return codec.decode(data)


def encode(typeof: CLType, value: object, encoding: CLEncoding = CLEncoding.BYTE_STREAM) -> typing.Union[ByteArray, ByteStream, HexString]:
    """Returns an instance of a domain type encoded as a byte array.

    :param typeof: Domain type to which data can be mapped, e.g. BOOL.
    :param value: Domain type instance to be encoded.
    :param encoding: A supported encoding.

    :returns: Domain instance appropriately encoded.

    """
    try:
        codec = CODECS[encoding]
    except KeyError:
        raise EncoderError(encoding, "Unsupported encoding.")  

    return codec.encode(typeof, value)
