from pycspr.litmus import cache
from pycspr.litmus.types import Block


def get_block_by_hash(block_id: bytes) -> Block:
    block: Block = cache.get_block_by_hash(block_id)
    if block is None:
        raise ValueError("TODO: call network")
    
    return block


def get_previous_switch_block(block_id: bytes):
    block: Block = cache.get_block_by_hash(block_id)
    if block is None:
        raise ValueError("Block not found")
    elif block.header.era_end is not None:
        return block
    else:
        return get_previous_switch_block(block.header.parent_hash)


def get_next_switch_block(block_id: int):
    block: Block = cache.get_block_by_height(block_id)
    if block is None:
        raise ValueError("Block not found")
    elif block.header.era_end is not None:
        return block
    else:
        return get_next_switch_block(block_id + 1)
