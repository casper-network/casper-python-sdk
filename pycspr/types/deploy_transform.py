import dataclasses
import enum
import typing


@dataclasses.dataclass
class NamedKey:
	pass


@dataclasses.dataclass
class Transform:
    """Base class for a state transformation occurring as an execution side effect.

    """
	pass


@dataclasses.dataclass
class AddInt32(Transform):
    value: int


@dataclasses.dataclass
class AddKeys(Transform):
    value: typing.List[NamedKey]


@dataclasses.dataclass
class AddUInt64(Transform):
    value: int


@dataclasses.dataclass
class AddUInt128(Transform):
    value: int


@dataclasses.dataclass
class AddUInt256(Transform):
    value: int


@dataclasses.dataclass
class AddUInt512(Transform):
    value: int
    

@dataclasses.dataclass
class Failure(Transform):
    value: str


@dataclasses.dataclass
class Identity(Transform):
	pass


@dataclasses.dataclass
class WriteAccount(Transform):
    value: bytes


@dataclasses.dataclass
class WriteBid(Transform):
    value: int


@dataclasses.dataclass
class WriteCLValue(Transform):
    value: int


@dataclasses.dataclass
class WriteContract(Transform):
    value: int


@dataclasses.dataclass
class WriteDeployInfo(Transform):
    value: int


@dataclasses.dataclass
class WriteEraInfo(Transform):
    value: int


@dataclasses.dataclass
class WriteTransfer(Transform):
    value: int


@dataclasses.dataclass
class WriteWithdraw(Transform):
    value: int
