import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.crypto import \
    KeyAlgorithm, \
    PublicKey, \
    PublicKeyBytes, \
    Signature, \
    SignatureBytes


def _decode_public_key(bytes_in: bytes) -> typing.Tuple[bytes, PublicKey]:
    _, algo = decode(KeyAlgorithm, bytes_in)
    rem, pbk = decode(PublicKeyBytes, bytes_in)

    return rem, PublicKey(algo, pbk)


def _decode_signature(bytes_in: bytes) -> typing.Tuple[bytes, Signature]:
    _, algo = decode(KeyAlgorithm, bytes_in)
    rem, sig = decode(SignatureBytes, bytes_in)

    return rem, Signature(algo, sig)


register_decoders({
    (PublicKey, _decode_public_key),
    (Signature, _decode_signature),
})
