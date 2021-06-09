from pycspr.types.deploy import PublicKey



def encode(entity: PublicKey) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return entity.hex()
