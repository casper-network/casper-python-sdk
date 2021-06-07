from pycspr.crypto.enums import KeyAlgorithm



# Map: key algorithm to key prefix.
_KEY_ALGO_PREFIX = {
    KeyAlgorithm.ED25519: "01",
    KeyAlgorithm.SECP256K1: "02",
}


def get_account_key(key_algo: KeyAlgorithm, public_key: str) -> str:
    """Returns an on-chain account key.

    :param key_algo: Algorithm used to generate ECC public key.
    :param public_key: Hexadecimal representation of an ECC public (aka verifying) key.

    :returns: An on-chain account key.

    """ 
    assert key_algo in _KEY_ALGO_PREFIX, \
           f"Unsupported key type: {key_algo}"

    if key_algo == KeyAlgorithm.ED25519:
        assert len(public_key) == 64, \
               "ED25519 public keys (hex format) should be 64 characters in length."
    if key_algo == KeyAlgorithm.SECP256K1:
        assert len(public_key) == 66, \
               "SECP256K1 public keys (hex format) should be 66 characters in length."

    return f"{_KEY_ALGO_PREFIX[key_algo]}{public_key}"


def get_account_key_algo(account_key: str) -> KeyAlgorithm:
    """Returns ECC algorithm associated with an account key.

    :param account_key: An account key from which associated ECC algorithm can be derived.

    :returns: An ECC key algorithm.

    """
    if account_key.startswith("01"):
        return KeyAlgorithm.ED25519
    if account_key.startswith("02"):
        return KeyAlgorithm.SECP256K1

    raise ValueError("Unsupported account key.")
