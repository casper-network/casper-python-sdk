from pycspr.codec._bytearray import cl_u32



def to_bytes(instance: bytearray) -> bytearray:
    """Maps bytearray to a bytearray for interpretation by a CSPR node.
    
    :param bytearray instance: A bytearray to be interpretated by a CSPR node.

    """
    return [cl_u32.encode(len(instance))] + instance
