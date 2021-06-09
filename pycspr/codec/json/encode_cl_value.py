from pycspr.types.cl import CLValue



def encode(entity: CLValue):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "TODO": entity.cl_type,
    }
