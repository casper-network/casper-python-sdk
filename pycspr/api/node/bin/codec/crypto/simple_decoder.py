import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.crypto import \
    DigestBytes, \
    KeyAlgorithm, \
    PublicKeyBytes, \
    SignatureBytes
from pycspr.api.node.bin.types.primitives.numeric import U8


def _decode_digest_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 32
    return bytes_in[32:], bytes_in[:32]


def _decode_key_algo(bytes_in: bytes) -> typing.Tuple[bytes, KeyAlgorithm]:
    assert len(bytes_in) >= 1
    rem, algo = decode(U8, bytes_in)
    return rem, KeyAlgorithm(algo)


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
    (PublicKeyBytes, _decode_public_key_bytes),
    (SignatureBytes, _decode_signature_bytes),
})
