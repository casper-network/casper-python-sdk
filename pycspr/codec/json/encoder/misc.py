import datetime

from pycspr.types import Digest
from pycspr.types import PublicKey
from pycspr.types import Signature
from pycspr.types import Timestamp



def encode_digest(entity: Digest) -> str:
    """Encodes a hash digest.

    """
    return entity.hex()


def encode_public_key(entity: PublicKey) -> str:
    """Encodes a public key.

    """
    return entity.account_key.hex()


def encode_signature(entity: Signature) -> str:
    """Encodes a payload signature.

    """
    return entity.hex()
    

def encode_timestamp(entity: Timestamp) -> str:
    """Encodes a millisecond precise timestamp.

    """
    timestamp_ms = round(entity, 3)
    timestamp_iso = datetime.datetime.utcfromtimestamp(timestamp_ms).isoformat()

    return f"{timestamp_iso[:-3]}Z"
