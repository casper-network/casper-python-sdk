import base64
import typing

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519



# Length of ED25519 private key in bytes.
_PVK_LENGTH = 32


def get_key_pair(seed: bytes = None) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :param seed: A seed used as input to deterministic key pair generation.

    :returns : 2 member tuple: (private key, public key)
    
    """
    sk = ed25519.Ed25519PrivateKey.generate() if seed is None else \
         ed25519.Ed25519PrivateKey.from_private_bytes(seed)

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
    
    """
    return ed25519.Ed25519PrivateKey.from_private_bytes(pvk).private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def get_pvk_from_pem_file(fpath: str) -> bytes:
    """Returns an ED25519 private key decoded from a PEM file.

    :param fpath: Path to a PEM file.

    :returns : Private key as byte array.
    
    """
    # Open pem file.
    with open(fpath, 'r') as fstream:
        as_pem = fstream.readlines()

    # Decode bytes.
    pvk_b64 = [l for l in as_pem if l and not l.startswith("-----")][0].strip()
    pvk = base64.b64decode(pvk_b64)
    
    return len(pvk) % _PVK_LENGTH == 0 and pvk[:_PVK_LENGTH] or pvk[-_PVK_LENGTH:]


def get_signature(data: bytes, pvk: bytes) -> bytes:
    """Returns an ED25519 digital signature of data signed from a PEM file representation of a private key.
    
    """
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(pvk)

    return sk.sign(data)


def get_signature_from_pem_file(data: bytes, fpath: str) -> bytes:
    """Returns an ED25519 digital signature of data signed from a PEM file representation of a private key.
    
    """
    return get_signature(data, get_pvk_from_pem_file(fpath))


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


def verify_signature(msg_hash: bytes, sig: bytes, vk: bytes) -> bool:
    """Returns a flag indicating whether a signature was signed by a signing key that is associated with the passed verification key.

    :param msg_hash: Previously signed message hash.
    :param sig: A digital signature.
    :param vk: Verifying key.
    :returns: A flag indicating whether a signature was signed by a signing key that is associated with the passed verification key.
    
    """
    raise NotImplementedError()
