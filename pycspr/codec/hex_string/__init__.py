from pycspr.codec import byte_array as byte_array_codec



def encode(entity: object) -> str:
    """Encodes a domain entity as a hexadecimal string.
    
    """    
    return byte_array_codec.encode(entity).hex()


def decode(entity: str) -> object:
    """Encodes a domain entity as a hexadecimal string.
    
    """    
    return byte_array_codec.decode(bytes.fromhex(entity))
