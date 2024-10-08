import typing

from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.api.node.bin.types.crypto import PublicKey


def _encode_public_key(entity: PublicKey) -> bytes:
    raise NotImplementedError()


register_encoders({
    (PublicKey, _encode_public_key),
})
