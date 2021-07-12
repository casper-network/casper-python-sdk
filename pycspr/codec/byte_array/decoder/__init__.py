import typing

import pycspr.codec.byte_array.decoder.cl as cl_decoder
import pycspr.codec.byte_array.decoder.deploy as deploy_decoder
from pycspr.types import CLType



def decode(typeof: typing.Union[CLType, object], as_bytes: typing.List[int]) -> object:
    """Decodes a domain entity from an array of bytes.
    
    """
    if isinstance(typeof, CLType):       
        return cl_decoder.decode(typeof, as_bytes) 
    else:
        return deploy_decoder.decode(typeof, as_bytes)
