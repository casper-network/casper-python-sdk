import base64
import typing

import ecdsa



# Curve of interest.
CURVE = ecdsa.SECP256k1

# Use uncompressed public keys.
UNCOMPRESSED = "uncompressed"


def get_key_pair(seed: bytes = None) -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair, each key is a 32 byte array.

    :returns : 2 member tuple: (private key, public key)
    
    """    
    sk = ecdsa.SigningKey.generate(curve=CURVE) if seed is None else \
         ecdsa.SigningKey.from_string(seed, curve=CURVE)

    return _get_key_pair(sk)


def get_key_pair_from_pem_file(fpath: str) -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair mapped from a PEM file representation of a private key.

    :param fpath: PEM file path.

    :returns : 2 member tuple: (private key, public key)
    
    """
    sk = _get_signing_key_from_pem_file(fpath)

    return _get_key_pair(sk)


def get_pvk_pem_from_bytes(pvk: bytes) -> bytes:
    """Returns SECP256K1 private key (pem) from bytes.
    
    """
    sk = ecdsa.SigningKey.from_string(pvk, curve=CURVE)

    return sk.to_pem()


def get_signature(data: bytes, pvk: bytes) -> bytes:
    """Returns an SECP256K1 digital signature of data signed from a PEM file representation of a private key.
    
    """
    return ecdsa.SigningKey.from_string(pvk, curve=CURVE).sign(data)


def get_signature_from_pem_file(data: bytes, fpath: str) -> bytes:
    """Returns an SECP256K1 digital signature of data signed from a PEM file representation of a private key.
    
    """
    sk = _get_signing_key_from_pem_file(fpath)

    return sk.sign(data)


def _get_key_pair(sk: ecdsa.SigningKey) -> typing.Tuple[bytes, bytes]:
    """Returns key pair from a signing key.
    
    """
    return sk.to_string(), \
           sk.verifying_key.to_string("compressed")


def _get_signing_key_from_pem_file(fpath: str) -> ecdsa.SigningKey:
    """Returns a signing key mapped from a PEM file representation of a private key.
    
    """
    with open(fpath, "rb") as f:
        return ecdsa.SigningKey.from_pem(f.read())


def verify_signature(msg_hash: bytes, sig: bytes, vk: bytes) -> bool:
    """Returns a flag indicating whether a signature was signed by a signing key that is associated with the passed verification key.

    :param msg_hash: Previously signed message hash.
    :param sig: A digital signature.
    :param vk: Verifying key.
    :returns: A flag indicating whether a signature was signed by a signing key that is associated with the passed verification key.
    
    """
    raise NotImplementedError()
