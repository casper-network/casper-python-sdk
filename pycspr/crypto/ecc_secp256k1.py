import hashlib
import typing

import ecdsa


# Default ECC + associated Casper specific hashing function.
_CURVE = ecdsa.SECP256k1
_HASH_FN = hashlib.sha256


def get_key_pair(seed: bytes = None) -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair, each key is a 32 byte array.

    :param seed: Entropy source to be used when geenrating key pair.
    :returns : 2 member tuple: (private key, public key)

    """
    if seed is None:
        sk = ecdsa.SigningKey.generate(curve=_CURVE)
    else:
        sk = ecdsa.SigningKey.from_string(seed, curve=_CURVE)

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

    :param pvk: A private key derived from a generated key pair.
    :returns: PEM represenation of signing key.

    """
    sk = ecdsa.SigningKey.from_string(pvk, curve=_CURVE)

    return sk.to_pem()


def get_signature(msg: bytes, pvk: bytes) -> bytes:
    """Returns an SECP256K1 digital signature of data signed from a private key PEM file.

    :param msg: A bunch of bytes to be signed.
    :param pvk: A private key derived from a generated key pair.
    :returns: A digital signature.

    """

    sk = ecdsa.SigningKey.from_string(pvk, curve=_CURVE)

    return sk.sign_deterministic(msg, hashfunc=_HASH_FN)


def get_signature_from_pem_file(msg: bytes, fpath: str) -> bytes:
    """Returns an SECP256K1 digital signature of data signed from a private key PEM file.

    :param msg: A bunch of bytes to be signed.
    :param fpath: PEM file path.
    :returns: A digital signature.

    """
    sk = _get_signing_key_from_pem_file(fpath)

    return sk.sign_deterministic(msg, hashfunc=_HASH_FN)


def is_signature_valid(msg: bytes, sig: bytes, pbk: bytes) -> bool:
    """Returns a flag indicating whether a signature was signed by a signing key
       associated with passed verification key.

    :param msg: A message that has apparently been signed.
    :param sig: A digital signature.
    :param pbk: Public key counterpart to generated private key.
    :returns: A flag indicating whether a signature was indeed signed by the signing key.

    """
    vk = ecdsa.VerifyingKey.from_string(pbk, curve=_CURVE)

    return vk.verify(sig, msg, hashfunc=_HASH_FN)


def _get_key_pair(sk: ecdsa.SigningKey) -> typing.Tuple[bytes, bytes]:
    """Returns key pair from a signing key.

    """
    return sk.to_string(), sk.verifying_key.to_string("compressed")


def _get_signing_key_from_pem_file(fpath: str) -> ecdsa.SigningKey:
    """Returns a signing key mapped from a PEM file representation of a private key.

    """
    with open(fpath, "rb") as fstream:
        return ecdsa.SigningKey.from_pem(fstream.read())
