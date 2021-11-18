import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey


@dataclasses.dataclass
class CL_Type_I32(CL_Type):
    """Encapsulates CL type information associated with a I32 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.I32

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "I32"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_I32":
        return CL_Type_I32()

    @staticmethod
    def from_json(_: str) -> "CL_Type_I32":
        return CL_Type_I32()


@dataclasses.dataclass
class CL_Type_I64(CL_Type):
    """Encapsulates CL type information associated with a I64 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.I64

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "I64"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_I64":
        return CL_Type_I64()

    @staticmethod
    def from_json(_: str) -> "CL_Type_I64":
        return CL_Type_I64()


@dataclasses.dataclass
class CL_Type_U8(CL_Type):
    """Encapsulates CL type information associated with a U8 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U8

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "U8"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_U8":
        return CL_Type_U8()

    @staticmethod
    def from_json(_: str) -> "CL_Type_U8":
        return CL_Type_U8()


@dataclasses.dataclass
class CL_Type_U32(CL_Type):
    """Encapsulates CL type information associated with a U32 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U32

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "U32"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_U32":
        return CL_Type_U32()

    @staticmethod
    def from_json(_: str) -> "CL_Type_U32":
        return CL_Type_U32()


@dataclasses.dataclass
class CL_Type_U64(CL_Type):
    """Encapsulates CL type information associated with a U64 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U64

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "U64"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_U64":
        return CL_Type_U64()

    @staticmethod
    def from_json(_: str) -> "CL_Type_U64":
        return CL_Type_U64()


@dataclasses.dataclass
class CL_Type_U128(CL_Type):
    """Encapsulates CL type information associated with a U128 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U128

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "U128"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_U128":
        return CL_Type_U128()

    @staticmethod
    def from_json(_: str) -> "CL_Type_U128":
        return CL_Type_U128()


@dataclasses.dataclass
class CL_Type_U256(CL_Type):
    """Encapsulates CL type information associated with a U256 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U256

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "U256"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_U256":
        return CL_Type_U256()

    @staticmethod
    def from_json(_: str) -> "CL_Type_U256":
        return CL_Type_U256()


@dataclasses.dataclass
class CL_Type_U512(CL_Type):
    """Encapsulates CL type information associated with a U512 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U512

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "U512"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_U512":
        return CL_Type_U512()

    @staticmethod
    def from_json(_: str) -> "CL_Type_U512":
        return CL_Type_U512()
