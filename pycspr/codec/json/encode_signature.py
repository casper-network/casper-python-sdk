from pycspr.types.deploy import Signature



def encode(entity: Signature) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return entity.hex()
