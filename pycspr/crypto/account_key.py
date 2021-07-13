from pycspr.crypto.enums import KeyAlgorithm



# Map: Key algorithm <-> length of public key.
_PUBLIC_KEY_LENGTHS = {
    KeyAlgorithm.ED25519: 32,
    KeyAlgorithm.SECP256K1: 33,
}


def get_account_key(key_algo: KeyAlgorithm, public_key: bytes) -> bytes:
    """Returns an on-chain account key.

    :param key_algo: Algorithm used to generate ECC public key.
    :param public_key: A byte array representation of an ECC public (aka verifying) key.
    :returns: An on-chain account key.

    """
    assert len(public_key) == _PUBLIC_KEY_LENGTHS[key_algo], \
           f"Invalid {key_algo.name} public key length."

    return bytes([key_algo.value]) + public_key


def get_account_key_algo(account_key: bytes) -> KeyAlgorithm:
    """Returns ECC algorithm identifier associated with an account key.

    :param account_key: An account key from which associated ECC algorithm identifier can be derived.
    :returns: An ECC key algorithm identifier.

    """
    try:
        return KeyAlgorithm(account_key[0])
    except ValueError:
        raise ValueError("Unsupported account key.")
