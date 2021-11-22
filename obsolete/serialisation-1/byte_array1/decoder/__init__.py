import typing

from pycspr.serialisation.byte_array.decoder.cl import decode as cl_decoder
from pycspr.serialisation.byte_array.decoder.deploy import decode as deploy_decoder
from pycspr.types import CLType


def decode(type_info: typing.Union[CLType, object], as_bytes: bytes) -> object:
    """Decodes a domain entity from an array of bytes.

    :param type_info: Encapsulate domain entity type information.
    :param as_bytes: Byte array entity representation.
    :returns: Decoded domain entity.

    """
    if isinstance(as_bytes, bytes):
        as_bytes = [i for i in as_bytes]
    elif isinstance(as_bytes, str):
        as_bytes = [i for i in bytes.fromhex(as_bytes)]

    if isinstance(type_info, CLType):
        return cl_decoder(type_info, as_bytes)
    else:
        return deploy_decoder(type_info, as_bytes)
