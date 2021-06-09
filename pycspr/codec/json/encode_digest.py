from pycspr.types.deploy import Digest



def encode(entity: Digest) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return entity.hex()
