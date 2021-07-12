import typing

from pycspr.codec.byte_array.encoder.cl import encode as cl_encoder
from pycspr.codec.byte_array.encoder.deploy import encode as deploy_encoder
from pycspr.types import CLValue



def encode(entity: object) -> typing.List[int]:
    """Encodes a domain entity as an array of bytes.
    
    """
    if type(entity) == CLValue:       
        return cl_encoder(entity) 
    else:
        return deploy_encoder(entity)
