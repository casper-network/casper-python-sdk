import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.type_defs.crypto import \
    DigestBytes, \
    KeyAlgorithm, \
    PublicKey, \
    PublicKeyBytes, \
    Signature, \
    SignatureBytes
from pycspr.type_defs.primitives import U8


def _decode_digest_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 32
    return bytes_in[32:], bytes_in[:32]


def _decode_key_algo(bytes_in: bytes) -> typing.Tuple[bytes, KeyAlgorithm]:
    assert len(bytes_in) >= 1
    rem, algo = decode(U8, bytes_in)
    return rem, KeyAlgorithm(algo)


def _decode_public_key(bytes_in: bytes) -> typing.Tuple[bytes, PublicKey]:
    _, algo = decode(KeyAlgorithm, bytes_in)
    rem, pbk = decode(PublicKeyBytes, bytes_in)

    return rem, PublicKey(algo, pbk)


def _decode_public_key_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    rem, algo = decode(KeyAlgorithm, bytes_in)
    if algo == KeyAlgorithm.ED25519:
        return rem[32:], rem[:32]
    elif algo == KeyAlgorithm.SECP256K1:
        return rem[33:], rem[:33]
    elif algo == KeyAlgorithm.SYSTEM:
        raise NotImplementedError(algo)
    else:
        raise ValueError("Invalid ECC algo type")


def _decode_signature(bytes_in: bytes) -> typing.Tuple[bytes, Signature]:
    _, algo = decode(KeyAlgorithm, bytes_in)
    rem, sig = decode(SignatureBytes, bytes_in)

    return rem, Signature(algo, sig)


def _decode_signature_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    rem, algo = decode(KeyAlgorithm, bytes_in)
    if algo in (KeyAlgorithm.ED25519, KeyAlgorithm.SECP256K1):
        return rem[64:], rem[:64]
    elif algo == KeyAlgorithm.SYSTEM:
        raise NotImplementedError(algo)
    else:
        raise ValueError("Invalid ECC algo type")


register_decoders({
    (DigestBytes, _decode_digest_bytes),
    (KeyAlgorithm, _decode_key_algo),
    (PublicKey, _decode_public_key),
    (PublicKeyBytes, _decode_public_key_bytes),
    (Signature, _decode_signature),
    (SignatureBytes, _decode_signature_bytes),
})
