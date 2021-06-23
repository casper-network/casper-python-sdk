from pycspr.codec.json import encoder
from pycspr.types.deploy import Deploy



# Map: entity type <-> encoder.
_ENCODERS = {
    Deploy: encoder.encode_deploy,
}


def encode(entity: object) -> str:
    """Maps domain entity to it's JSON representation.
    
    :param entity: A domain entity.
    :returns: JSON encoded representation.

    """
    return _ENCODERS[type(entity)](entity)
