from pycspr.crypto.ecc import get_signature
from pycspr.crypto.ecc import is_signature_valid
from pycspr.crypto.hashifier import get_hash
from pycspr.types.crypto.complex import PrivateKey
from pycspr.types.crypto.simple import Digest
from pycspr.types.crypto.simple import HashAlgorithm
from pycspr.types.crypto.simple import KeyAlgorithm
from pycspr.types.crypto.simple import SignatureBytes


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
    key_algo: KeyAlgorithm = KeyAlgorithm(account_key[0])
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


def get_signature_for_deploy_approval(
    deploy_hash: Digest,
    key_of_approver: PrivateKey
) -> SignatureBytes:
    """Returns a signature designated to approve a deploy.

    :param deploy_hash: Digest of a deploy to be signed.
    :param key_of_approver: Private key of approver.
    :returns: Digital signature over deploy digest.

    """
    return \
        bytes([key_of_approver.algo.value]) + \
        get_signature(deploy_hash, key_of_approver.pvk, key_of_approver.algo)


def verify_deploy_approval_signature(
    deploy_hash: Digest,
    sig: SignatureBytes,
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

    return is_signature_valid(
        deploy_hash,
        sig[1:],
        account_key[1:],
        KeyAlgorithm(account_key[0])
        )
