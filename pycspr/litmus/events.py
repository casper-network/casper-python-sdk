from pycspr.litmus.types import BlockHash
# from pycspr.litmus.types import Kernel


def on_block_finalisation(block_id: BlockHash):
    print(block_id)

