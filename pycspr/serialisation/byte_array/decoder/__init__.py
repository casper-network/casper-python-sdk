import typing

import pycspr.serialisation.byte_array.decoder.cl as cl_decoder
import pycspr.serialisation.byte_array.decoder.deploy as deploy_decoder
from pycspr.types import CLType



def decode(typeof: typing.Union[CLType, object], as_bytes: bytes) -> object:
    """Decodes a domain entity from an array of bytes.
    
    """
    as_hex = as_bytes.hex()

    if isinstance(as_bytes, bytes):
        as_bytes = [i for i in as_bytes]
    elif isinstance(as_bytes, str):
        as_bytes = [i for i in bytes.fromhex(as_bytes)]

    if isinstance(typeof, CLType):
        return cl_decoder.decode(typeof, as_bytes) 
    else:
        return deploy_decoder.decode(typeof, as_bytes)
