import json

from pycspr.serialisation.dictionary.decoder.deploy import decode_deploy as decode_deploy_from_dict
from pycspr.types import Deploy



def decode(entity: str) -> Deploy:
    """Decodes a domain entity from a JSON text blob.
    
    """
    return decode_deploy_from_dict(json.loads(entity))
