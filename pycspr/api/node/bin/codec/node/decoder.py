from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.node import NodeUptime
from pycspr.api.node.bin.types.primitives.numeric import U64


register_decoders({
    (NodeUptime, lambda x: decode(x, U64)),
})
