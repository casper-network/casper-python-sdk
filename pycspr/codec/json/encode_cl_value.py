from pycspr.types.cl import CLValue
from pycspr.codec.byte_array import encode as to_byte_array
from pycspr.codec.json.encode_cl_type import encode as encode_cl_type
from pycspr.codec.json.encode_digest import encode as encode_digest



def encode(entity: CLValue):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "bytes": bytes(to_byte_array(entity)).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": str(entity.parsed),
    }
