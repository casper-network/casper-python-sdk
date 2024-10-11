from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.chain.simple import \
    BlockBodyHash, \
    BlockHash, \
    BlockHeight, \
    ChainNameDigest, \
    DelegationRate, \
    EraID, \
    GasPrice, \
    Motes, \
    Weight
from pycspr.api.node.bin.types.crypto import DigestBytes
from pycspr.api.node.bin.types.primitives.numeric import U8, U64, U512


register_decoders({
    (BlockBodyHash, lambda x: decode(DigestBytes, x)),
    (BlockHash, lambda x: decode(DigestBytes, x)),
    (BlockHeight, lambda x: decode(U64, x)),
    (ChainNameDigest, lambda x: decode(DigestBytes, x)),
    (DelegationRate, lambda x: decode(U8, x)),
    (EraID, lambda x: decode(U64, x)),
    (GasPrice, lambda x: decode(U8, x)),
    (Motes, lambda x: decode(U512, x)),
    (Weight, lambda x: decode(U512, x)),
})
