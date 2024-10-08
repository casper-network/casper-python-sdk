import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.crypto import \
    DigestBytes, \
    KeyAlgorithm, \
    PublicKeyBytes
from pycspr.api.node.bin.types.primitives.numeric import U8


def _decode_digest_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 32
    return bytes_in[32:], bytes_in[:32]


def _decode_key_algo(bytes_in: bytes) -> typing.Tuple[bytes, KeyAlgorithm]:
    assert len(bytes_in) >= 1
    bytes_rem, algo_type = decode(U8, bytes_in)
    return bytes_rem, KeyAlgorithm(algo_type)


def _decode_public_key_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    bytes_rem, key_algo = decode(KeyAlgorithm, bytes_in)
    if key_algo == KeyAlgorithm.ED25519:
        return bytes_rem[32:], bytes_rem[:32]
    elif key_algo == KeyAlgorithm.ED25519:
        return bytes_rem[33:], bytes_rem[:33]
    elif key_algo == KeyAlgorithm.SYSTEM:
        return bytes_rem, bytes([])
    else:
        raise ValueError("Invalid ECC key algo type")


register_decoders({
    (DigestBytes, _decode_digest_bytes),
    (KeyAlgorithm, _decode_key_algo),
    (PublicKeyBytes, _decode_public_key_bytes),
})
