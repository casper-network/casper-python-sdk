from pycspr.litmus.kernel import Kernel
from pycspr.litmus.types import BlockHash


def create_kernel(block_id: BlockHash):
    return Kernel(block_id)
