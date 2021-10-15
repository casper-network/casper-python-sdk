from pycspr.crypto.ecc import get_signature
from pycspr.crypto.ecc import is_signature_valid
from pycspr.crypto.enums import HashAlgorithm
from pycspr.crypto.enums import KeyAlgorithm
from pycspr.crypto.hashifier import get_hash


# Desired length of hash digest.
_DIGEST_LENGTH = 32

# Map: Key algorithm <-> length of public key.
_PUBLIC_KEY_LENGTHS = {
    KeyAlgorithm.ED25519: 32,
    KeyAlgorithm.SECP256K1: 33,
}


def get_account_hash(account_key: bytes) -> bytes:
    """Returns an on-chain account identifier (hex format) as derived from an account key.

    :param account_key: An on-chain account identifier.

    :returns: An on-chain account identifier.

    """
    key_algo: KeyAlgorithm = get_account_key_algo(account_key)
    public_key: bytes = account_key[1:]
    as_bytes: bytes = \
        bytes(key_algo.name.lower(), "utf-8") + \
        bytearray(1) + \
        public_key

    return get_hash(as_bytes, _DIGEST_LENGTH, HashAlgorithm.BLAKE2B)


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

    :param account_key: An account key associated with a specific ECC algorithm.
    :returns: An ECC key algorithm identifier.

    """
    try:
        return KeyAlgorithm(account_key[0])
    except ValueError:
        raise ValueError("Unsupported account key.")


def get_signature_for_deploy_approval(
    deploy_hash: bytes,
    private_key: bytes,
    key_algo: KeyAlgorithm
) -> bytes:
    """Returns a signature designated to approve a deploy.

    :param deploy_hash: Identifier, i.e. hash, of a deploy to be signed.
    :param pvk: Secret key.
    :param algo: Type of ECC algo used to generate secret key.
    :returns: Digital signature of input data.

    """
    return bytes([key_algo.value]) + get_signature(deploy_hash, private_key, algo=key_algo)


def verify_deploy_approval_signature(
    deploy_hash: bytes,
    sig: bytes,
    account_key: bytes
) -> bool:
    """Returns a flag indicating whether a deploy signature was signed by private key
       associated with the passed account key.

    :param deploy_hash: Hash of a deploy that has been signed.
    :param sig: A digital signature.
    :param account_key: An account key associated with an ECC algorithm.
    :returns: A flag indicating whether a deploy signature was signed by private key.

    """
    assert len(deploy_hash) == 32, \
           "Invalid deploy hash.  Expected length = 32"
    assert len(sig) == 65, \
           "Invalid deploy approval signature.  Expected length = 65"

    algo = get_account_key_algo(account_key)

    return is_signature_valid(deploy_hash, sig[1:], account_key[1:], algo)
