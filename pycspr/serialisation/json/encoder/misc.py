import datetime

from pycspr.types import Digest
from pycspr.types import PublicKey
from pycspr.types import Signature
from pycspr.types import Timestamp



def encode_account_key(entity: bytes) -> str:
    """Encodes an on-chain account key.

    """
    return entity.hex()


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
    as_ts_3_decimal_places = round(entity, 3)
    as_datetime = datetime.datetime.fromtimestamp(as_ts_3_decimal_places, tz=datetime.timezone.utc)
    as_iso = as_datetime.isoformat()

    return f"{as_iso[:-9]}Z"
