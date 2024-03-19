from pycspr.litmus.types import Block
from pycspr.litmus.digests import get_digest_of_block



class VerificationError(Exception):
    pass


def verify_block(block: Block):
    # TODO: recompute hash and assert equivalence.
    assert get_digest_of_block(block.header) == block.hash


def verify_block_body(block: Block):
    # TODO: recompute hash and assert equivalence.
    
    assert block.header.body_hash == block.header.body_hash
