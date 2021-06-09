from pycspr.types.cl import CLValue
from pycspr.codec.json.encode_cl_type import encode as encode_cl_type



def encode(entity: CLValue):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "bytes": entity.bytes.hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": str(entity.parsed),
    }
