from pycspr.api.node.bin.codec.utils import register_encoders
from pycspr.crypto.types import PublicKey


register_encoders({
    (PublicKey, lambda x: bytes([x.algo.value]) + x.pbk),
})
