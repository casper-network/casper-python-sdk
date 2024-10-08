import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.crypto import \
    KeyAlgorithm, \
    PublicKey, \
    PublicKeyBytes


def _decode_public_key(bytes_in: bytes) -> typing.Tuple[bytes, PublicKey]:
    bytes_rem, algo = decode(KeyAlgorithm, bytes_in)
    bytes_rem, pbk = decode(PublicKeyBytes, bytes_in)

    return bytes_rem, PublicKey(algo, pbk)


register_decoders({
    (PublicKey, _decode_public_key),
})
