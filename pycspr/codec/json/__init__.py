import json

from pycspr.codec.json.encoder_deploy import encode_deploy
from pycspr.codec.json.decoder_deploy import decode_deploy as decode
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
    else:
        return json.dumps(encoder(entity), indent=4)