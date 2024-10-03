from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.chain.simple import \
    BlockBodyHash, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    GasPrice, \
    Motes, \
    Weight
from pycspr.api.node.bin.types.primitives.crypto import DigestBytes
from pycspr.api.node.bin.types.primitives.numeric import U8, U64, U512


register_decoders({
    (BlockBodyHash, lambda x: decode(x, DigestBytes)),
    (BlockHash, lambda x: decode(x, DigestBytes)),
    (BlockHeight, lambda x: decode(x, U64)),
    (EraID, lambda x: decode(x, U64)),
    (GasPrice, lambda x: decode(x, U8)),
    (Motes, lambda x: decode(x, U512)),
    (Weight, lambda x: decode(x, U512)),
})
