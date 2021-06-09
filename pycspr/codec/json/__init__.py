from pycspr.codec.json.encode_deploy import encode as encode_deploy
from pycspr.types.deploy import Deploy



# Map: entity type <-> encoder.
_ENCODERS = {
    Deploy: encode_deploy,
}


def encode(entity: object):
    return _ENCODERS[type(entity)](entity)
