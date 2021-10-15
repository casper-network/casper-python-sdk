import base64
import typing

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


# Length of ED25519 private key in bytes.
_PVK_LENGTH = 32


def get_key_pair(seed: bytes = None) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :param seed: A seed used as input to deterministic key pair generation.
    :returns : 2 member tuple: (private key, public key)

    """
    if seed is None:
        sk = ed25519.Ed25519PrivateKey.generate()
    else:
        sk = ed25519.Ed25519PrivateKey.from_private_bytes(seed)

    return _get_key_pair(sk)


def get_key_pair_from_pem_file(fpath: str) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair mapped from a PEM file representation of a private key.

    :param fpath: PEM file path.
    :returns : 2 member tuple: (private key, public key)

    """
    pvk = get_pvk_from_pem_file(fpath)

    return get_key_pair(pvk)


def get_pvk_pem_from_bytes(pvk: bytes) -> bytes:
    """Returns ED25519 private key (pem) from bytes.

    :param pvk: A private key derived from a generated key pair.
    :returns: PEM represenation of signing key.

    """
    return ed25519.Ed25519PrivateKey.from_private_bytes(pvk).private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def get_pvk_from_pem_file(fpath: str) -> bytes:
    """Returns an ED25519 private key decoded from a PEM file.

    :param fpath: Path to a PEM file.
    :returns: A private key.

    """
    # Open pem file.
    with open(fpath, 'r') as fstream:
        as_pem = fstream.readlines()

    # Decode bytes.
    pvk_b64 = [i for i in as_pem if i and not i.startswith("-----")][0].strip()
    pvk = base64.b64decode(pvk_b64)

    return len(pvk) % _PVK_LENGTH == 0 and pvk[:_PVK_LENGTH] or pvk[-_PVK_LENGTH:]


def get_signature(msg: bytes, pvk: bytes) -> bytes:
    """Returns an ED25519 digital signature of data signed from a private key PEM file.

    :param msg: A bunch of bytes to be signed.
    :param pvk: A private key derived from a generated key pair.
    :returns: A digital signature.

    """
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(pvk)

    return sk.sign(msg)


def get_signature_from_pem_file(msg: bytes, fpath: str) -> bytes:
    """Returns an ED25519 digital signature of data signed from a private key PEM file.

    :param msg: A bunch of bytes to be signed.
    :param fpath: PEM file path.
    :returns: A digital signature.

    """
    return get_signature(msg, get_pvk_from_pem_file(fpath))


def is_signature_valid(msg_hash: bytes, sig: bytes, pbk: bytes) -> bool:
    """Returns a flag indicating whether a signature was signed by a signing key.

    :param msg_hash: Previously signed message hash.
    :param sig: A digital signature.
    :param pbk: Public verifying key.
    :returns: A flag indicating whether a signature was signed by a signing key.

    """
    vk = ed25519.Ed25519PublicKey.from_public_bytes(pbk)
    try:
        vk.verify(sig, msg_hash)
    except InvalidSignature:
        return False
    else:
        return True


def _get_key_pair(sk: ed25519.Ed25519PrivateKey) -> typing.Tuple[bytes, bytes]:
    """Returns key pair from a signing key.

    """
    pk = sk.public_key()

    return \
        sk.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ), \
        pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
