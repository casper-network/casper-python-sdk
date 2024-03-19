import enum


class AssymetricKeyType(enum.Enum):
    PRIVATE = enum.auto()
    PUBLIC = enum.auto()


class AccountType(enum.Enum):
    FAUCET = enum.auto()
    USER = enum.auto()
    VALIDATOR = enum.auto()


class NodePortType(enum.Enum):
    RPC = enum.auto()
    RPC_SPECULATIVE = enum.auto()
    REST = enum.auto()
    SSE = enum.auto()
