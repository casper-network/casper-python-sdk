from pycspr.types.deploy import Timestamp



def encode(entity: Timestamp) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return f"{entity.isoformat()}Z"
