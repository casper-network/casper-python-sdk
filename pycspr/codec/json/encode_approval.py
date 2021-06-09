from pycspr.types.deploy import Approval
from pycspr.codec.json.encode_public_key import encode as encode_public_key
from pycspr.codec.json.encode_signature import encode as encode_signature



def encode(entity: Approval):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "signer": encode_public_key(entity.signer),
        "signature": encode_signature(entity.signature),
    }
