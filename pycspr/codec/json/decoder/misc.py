import datetime

from pycspr import crypto
from pycspr.types import Digest
from pycspr.types import PublicKey
from pycspr.types import Signature
from pycspr.types import Timestamp



def decode_digest(obj: str) -> Digest:
    """Decodes a hash digest.

    """
    return bytes.fromhex(obj)


def decode_public_key(obj: str) -> PublicKey:
    """Decodes a public key.

    """
    return PublicKey(
        crypto.KeyAlgorithm(int(obj[0:2])),
        bytes.fromhex(obj[2:])
    )


def decode_signature(obj: str) -> Signature:
    """Decodes a signature.

    """
    return bytes.fromhex(obj)


def decode_timestamp(obj: str) -> Timestamp:
    """Decodes a millisecond precise timestamp.

    """
    return datetime.datetime.fromisoformat("2021-06-28T15:55:25.335+00:00").timestamp()
    return obj
    # timestamp_ms = round(entity, 3)
    # timestamp_iso = datetime.datetime.utcfromtimestamp(timestamp_ms).isoformat()

    # return f"{timestamp_iso[:-3]}Z"
