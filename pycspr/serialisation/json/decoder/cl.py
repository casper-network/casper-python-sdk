import typing

from pycspr.serialisation.byte_array import decode as byte_array_decoder
from pycspr.types import CLValue
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple


# Map: simple type keys to internal enum.
_SIMPLE_TYPE_TO_ENUM = {
    "Bool": CLTypeKey.BOOL,
    "Unit": CLTypeKey.UNIT,
    "String": CLTypeKey.STRING,
    "Key": CLTypeKey.KEY,
    "URef": CLTypeKey.UREF,
    "PublicKey": CLTypeKey.PUBLIC_KEY,
}


def decode_cl_type(obj) -> CLType:
    """Decodes a CL type definition.

    """
    def _decode_byte_array():
        return CLType_ByteArray(size=obj["ByteArray"])

    def _decode_option():
        return CLType_Option(inner_type=decode_cl_type(obj["Option"]))

    def _decode_simple():
        try:
            type_key = _SIMPLE_TYPE_TO_ENUM[obj]
        except KeyError:
            type_key = CLTypeKey[obj]
        finally:
            return CLType_Simple(type_key=type_key)

    # Set decoder.
    if isinstance(obj, dict):
        if "ByteArray" in obj:
            decoder = _decode_byte_array
        elif "Option" in obj:
            decoder = _decode_option
        else:
            raise NotImplementedError()
    else:
        decoder = _decode_simple

    return decoder()


def decode_cl_value(obj: typing.Union[dict, str]) -> CLValue:
    """Decodes a CL value.

    """
    cl_type = decode_cl_type(obj["cl_type"])
    as_bytes = bytes.fromhex(obj["bytes"])
    if isinstance(cl_type, (CLType_Simple, CLType_ByteArray, CLType_Option)):
        parsed = byte_array_decoder(cl_type, as_bytes)
    else:
        parsed = None

    return CLValue(cl_type, parsed, as_bytes)
