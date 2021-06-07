from pycspr.crypto.account_key import get_account_key_algo
from pycspr.crypto.enums import HashAlgorithm
from pycspr.crypto.enums import HashEncoding
from pycspr.crypto.enums import KeyAlgorithm
from pycspr.crypto.hashifier import get_hash



# Desired length of hash digest.
_DIGEST_LENGTH = 32


def get_account_hash(account_key: str) -> str:
    """Returns an on-chain account identifier (hex format) as derived from an account key.

    :param account_key: An on-chain account identifier.

    :returns: An on-chain account identifier.

    """
    key_algo: KeyAlgorithm = get_account_key_algo(account_key)
    public_key: str = account_key[2:]

    as_bytes: bytes = \
        bytes(key_algo.name.lower(), "utf-8") + \
        bytearray(1) + \
        bytes.fromhex(public_key)

    return get_hash(as_bytes, _DIGEST_LENGTH, HashAlgorithm.BLAKE2B, HashEncoding.HEX)
