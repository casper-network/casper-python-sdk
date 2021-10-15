import json

from pycspr.serialisation.json.encoder.deploy import encode_deploy
from pycspr.types import Deploy


# Map: entity type <-> encoder.
_ENCODERS = {
    Deploy: encode_deploy,
}


def encode(entity: object) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: A domain entity.
    :returns: JSON encoded representation.

    """
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unencodeable type: {type(entity)}")

    return json.dumps(encoder(entity))
