from pycspr.types.deploy import ExecutionArgument
from pycspr.codec.json.encode_cl_value import encode as encode_cl_value



def encode(entity: ExecutionArgument):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return [
        entity.name,
        encode_cl_value(entity.value)
    ]
