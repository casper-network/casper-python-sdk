from pycspr.api.node.bin.codec.utils import decode, register_decoder
from pycspr.api.node.bin.types.domain import NodeUptime
from pycspr.api.node.bin.types.primitives import U64


register_decoder(NodeUptime, lambda x: decode(x, U64))
