from pycspr.types.cl import CLValue
from pycspr.codec import byte_array
from pycspr.codec.json.encode_cl_type import encode as encode_cl_type
from pycspr.codec.json.encode_digest import encode as encode_digest






def encode(entity: CLValue):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    print(entity.cl_type.typeof, byte_array.encode(entity))

    return {
        "bytes": bytes(byte_array.encode(entity)).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": str(entity.parsed),
    }
