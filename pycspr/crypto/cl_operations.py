from pycspr.crypto.ecc import get_signature
from pycspr.crypto.ecc import is_signature_valid
from pycspr.crypto.hashifier import get_hash
from pycspr.type_defs.crypto import DigestBytes
from pycspr.type_defs.crypto import HashAlgorithm
from pycspr.type_defs.crypto import KeyAlgorithm
from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.crypto import PrivateKey
from pycspr.type_defs.crypto import Signature


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


# Synonym to correct domain pollution.
get_account_address = get_account_hash


def get_account_key(algo: KeyAlgorithm, pbk: bytes) -> bytes:
    """Returns an on-chain account key.

    :param algo: Algorithm used to generate ECC public key.
    :param pbk: A byte array representation of an ECC public (aka verifying) key.
    :returns: An on-chain account key.

    """
    assert len(pbk) == _PUBLIC_KEY_LENGTHS[algo], \
           f"Invalid {algo.name} public key length."

    return bytes([algo.value]) + pbk


def get_signature_for_deploy_approval(digest: DigestBytes, approver: PrivateKey) -> Signature:
    """Returns a signature designated to approve a deploy.

    :param digest: Digest of a deploy to be signed.
    :param key_of_approver: Private key of approver.
    :returns: Digital signature over deploy digest.

    """
    return Signature(
        approver.algo,
        get_signature(digest, approver.algo, approver.pvk)
        )


def verify_deploy_approval_signature(
    deploy_hash: DigestBytes,
    signature: Signature,
    account_public_key: PublicKey,
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
    assert len(signature.to_bytes()) == 65, \
           "Invalid deploy approval signature.  Expected length = 65"

    return is_signature_valid(
        deploy_hash,
        signature.algo,
        signature.sig,
        account_public_key.pbk,
        )
