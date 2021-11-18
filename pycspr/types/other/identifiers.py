import typing


# An account identifier may be a byte array of 33 bytes,
# a hexadecimal string of 66 characters.
AccountIdentifer = typing.Union[bytes, str]

# A block identifier may be a byte array of 32 bytes,
# a hexadecimal string of 64 characters or a positive integer.
BlockIdentifer = typing.Union[bytes, str, int]

# On chain contract identifier.
ContractIdentifer = typing.NewType("Static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# A deploy identifier is a 32 byte array or it's hexadecimal string equivalent.
DeployIdentifer = typing.Union[bytes, str]

# Root hash of a node's global state.
StateRootIdentifier = typing.NewType(
    "Cumulative hash of block execution effects over global state.",
    bytes
    )
