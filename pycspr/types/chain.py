import typing


# A block identifier may be a byte array of 32 bytes,
# a hexadecimal string of 64 characters or a positive integer.
BlockIdentifer = typing.Union[bytes, str, int]

# An optional block identifier.
OptionalBlockIdentifer = typing.Union[None, BlockIdentifer]

# Root hash of a node's global state.
StateRootHash = typing.NewType(
    "Cumulative hash of block execution effects over global state.", bytes)

# An optional state root hash.
OptionalStateRootHash = typing.Union[None, StateRootHash]
