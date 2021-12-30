from pycspr.crypto import cl_checksum
from pycspr.types import cl_values
from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.serialisation.cl_value_to_cl_type import encode as cl_value_to_cl_type
from pycspr.serialisation.cl_type_to_json import encode as cl_type_to_json
from pycspr.serialisation.cl_value_to_parsed import encode as cl_value_to_parsed


def encode(entity: cl_values.CL_Value) -> dict:
    """Encodes a CL value as a JSON compatible dictionary.

    :param entity: A CL value to be encoded.
    :returns: A JSON compatible dictionary.
    
    """
    return {
        "cl_type": cl_type_to_json(cl_value_to_cl_type(entity)),
        "bytes": cl_checksum.encode(cl_value_to_bytes(entity)),
        "parsed": cl_value_to_parsed(entity)
    }
