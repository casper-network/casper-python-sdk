import typing

from pycspr.serialisation.byte_array.encoder.cl import encode as encode_cl_value
from pycspr.serialisation.byte_array.encoder.deploy import encode as encode_deploy
from pycspr.types import CLValue



def encode(entity: object) -> bytes:
    """Encodes a domain entity as an array of bytes.
    
    """
    if type(entity) == CLValue:       
        return encode_cl_value(entity) 
    else:
        return encode_deploy(entity)
