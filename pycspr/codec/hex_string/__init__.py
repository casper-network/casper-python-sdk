from pycspr.codec import byte_array



def encode(entity: object) -> str:
    """Encodes a domain entity as a hexadecimal string.
    
    """    
    return bytes(byte_array.encode(entity)).hex()
