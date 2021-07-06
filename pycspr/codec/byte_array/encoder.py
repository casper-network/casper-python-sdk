import typing

from pycspr.codec.byte_array.encoder_cl import encode as encoder_cl
from pycspr.codec.byte_array.encoder_deploy import encode as encoder_deploy
from pycspr.types.cl import CLValue



def encode(value) -> typing.List[int]:
    """Encodes a domain value as an array of bytes.
    
    """
    if type(value) == CLValue:       
        return encoder_cl(value) 
    else:
        return encoder_deploy(value) 
