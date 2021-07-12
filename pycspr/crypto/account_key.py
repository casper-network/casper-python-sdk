from pycspr.crypto.enums import KeyAlgorithm



# Map: key algorithm to key prefix.
_KEY_ALGO_PREFIX = {
    KeyAlgorithm.ED25519: bytes([1]),
    KeyAlgorithm.SECP256K1: bytes([2]),
}


def get_account_key(key_algo: KeyAlgorithm, public_key: bytes) -> bytes:
    """Returns an on-chain account key.

    :param key_algo: Algorithm used to generate ECC public key.
    :param public_key: A byte array representation of an ECC public (aka verifying) key.

    :returns: An on-chain account key.

    """ 
    assert key_algo in _KEY_ALGO_PREFIX, f"Unsupported key type: {key_algo}"
    assert key_algo == KeyAlgorithm.ED25519 and len(public_key) == 32 or \
           key_algo == KeyAlgorithm.SECP256K1 and len(public_key) == 33, \
           "Invalid key length."

    return _KEY_ALGO_PREFIX[key_algo] + public_key


def get_account_key_algo(account_key: bytes) -> KeyAlgorithm:
    """Returns ECC algorithm associated with an account key.

    :param account_key: An account key from which associated ECC algorithm can be derived.

    :returns: An ECC key algorithm.

    """
    if account_key[0] == 1:
        return KeyAlgorithm.ED25519
    elif account_key[0] == 2:
        return KeyAlgorithm.SECP256K1
    else:
        raise ValueError("Unsupported account key.")
