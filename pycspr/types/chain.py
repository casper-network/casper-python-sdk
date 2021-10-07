from typing import Union, NewType

# A block identifier may be a byte array of 32 bytes,
# a hexadecimal string of 64 characters or a positive integer.
# @TODO: wrong spelling, change it!
BlockIdentifer = Union[bytes, str, int]

# NOT NEEDED! same as block_id: BlockIdentifer = None
OptionalBlockIdentifer = Union[None, BlockIdentifer]

# Root hash of a node's global state.
# @TODO: Why complicating things with a special name for bytes???
#   Not necassary and confusing, use byte instead ....
StateRootHash = NewType(
    "32 byte array calculated by a node when "
    "applying block execution effects over global state.",
    bytes
)

# An optional state root hash.
OptionalStateRootHash = Union[None, StateRootHash]
