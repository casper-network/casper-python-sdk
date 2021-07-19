import json

from pycspr.serialisation.dictionary.encoder.deploy import encode_deploy as encode_deploy_as_dict
from pycspr.types import Deploy



def encode(entity: Deploy) -> str:
    """Maps a domain entity to a dictionary and then emits the JSON representation.
    
    :param entity: A domain entity.
    :returns: JSON encoded representation.

    """
    return json.dumps(encode_deploy_as_dict(entity))
