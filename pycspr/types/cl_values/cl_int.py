import dataclasses

from pycspr.types.cl_types import CL_Type_I32
from pycspr.types.cl_types import CL_Type_I64
from pycspr.types.cl_types import CL_Type_U8
from pycspr.types.cl_types import CL_Type_U32
from pycspr.types.cl_types import CL_Type_U64
from pycspr.types.cl_types import CL_Type_U128
from pycspr.types.cl_types import CL_Type_U256
from pycspr.types.cl_types import CL_Type_U512
from pycspr.types.cl_values.base import CL_Value
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import le_bytes_to_int


@dataclasses.dataclass
class CL_I32(CL_Value):
    """Represents a CL type value: I32.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        return int_to_le_bytes(self.value, 4, True)

    def as_cl_type(self) -> CL_Type_I32:
        return CL_Type_I32()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_I32":
        return CL_I32(le_bytes_to_int(as_bytes, True))

    #endregion


@dataclasses.dataclass
class CL_I64(CL_Value):
    """Represents a CL type value: I64.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        return int_to_le_bytes(self.value, 8, True)

    def as_cl_type(self) -> CL_Type_I64:
        return CL_Type_I64()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_I64":
        return CL_I64(le_bytes_to_int(as_bytes, True))

    #endregion


@dataclasses.dataclass
class CL_U8(CL_Value):
    """Represents a CL type value: U8.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        return int_to_le_bytes(self.value, 1, False)

    def as_cl_type(self) -> CL_Type_U8:
        return CL_Type_U8()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U8":
        return CL_U8(le_bytes_to_int(as_bytes, False))

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 8) - 1

    #endregion


@dataclasses.dataclass
class CL_U32(CL_Value):
    """Represents a CL type value: U32.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        return int_to_le_bytes(self.value, 4, False)

    def as_cl_type(self) -> CL_Type_U32:
        return CL_Type_U32()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U32":
        return CL_U32(le_bytes_to_int(as_bytes, False))

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 32) - 1

    #endregion


@dataclasses.dataclass
class CL_U64(CL_Value):
    """Represents a CL type value: U64.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        return int_to_le_bytes(self.value, 8, False)

    def as_cl_type(self) -> CL_Type_U64:
        return CL_Type_U64()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U64":
        return CL_U64(le_bytes_to_int(as_bytes, False))

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 64) - 1

    #endregion


@dataclasses.dataclass
class CL_U128(CL_Value):
    """Represents a CL type value: U128.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        if CL_U8.is_in_range(self.value):
            byte_length = 1
        elif CL_U32.is_in_range(self.value):
            byte_length = 4
        elif CL_U64.is_in_range(self.value):
            byte_length = 8
        elif CL_U128.is_in_range(self.value):
            byte_length = 16
        else:
            raise ValueError("Invalid U128: max size exceeded")
        
        return int_to_le_bytes(self.value, byte_length, False)

    def as_cl_type(self) -> CL_Type_U128:
        return CL_Type_U128()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U128":
        return CL_U128(le_bytes_to_int(as_bytes, False))

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 128) - 1

    #endregion


@dataclasses.dataclass
class CL_U256(CL_Value):
    """Represents a CL type value: U256.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        if CL_U8.is_in_range(self.value):
            byte_length = 1
        elif CL_U32.is_in_range(self.value):
            byte_length = 4
        elif CL_U64.is_in_range(self.value):
            byte_length = 8
        elif CL_U128.is_in_range(self.value):
            byte_length = 16
        elif CL_U256.is_in_range(self.value):
            byte_length = 32
        else:
            raise ValueError("Invalid U256: max size exceeded")
        
        return int_to_le_bytes(self.value, byte_length, False)

    def as_cl_type(self) -> CL_Type_U256:
        return CL_Type_U256()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U256":
        return CL_U256(le_bytes_to_int(as_bytes, False))

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 256) - 1

    #endregion


@dataclasses.dataclass
class CL_U512(CL_Value):
    """Represents a CL type value: U512.
    
    """
    # Associated value.
    value: int

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        if CL_U8.is_in_range(self.value):
            byte_length = 1
        elif CL_U32.is_in_range(self.value):
            byte_length = 4
        elif CL_U64.is_in_range(self.value):
            byte_length = 8
        elif CL_U128.is_in_range(self.value):
            byte_length = 16
        elif CL_U256.is_in_range(self.value):
            byte_length = 32
        elif CL_U512.is_in_range(self.value):
            byte_length = 64
        else:
            raise ValueError("Invalid U512: max size exceeded")
        
        return int_to_le_bytes(self.value, byte_length, False)

    def as_cl_type(self) -> CL_Type_U512:
        return CL_Type_U512()

    def as_parsed(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U512":
        return CL_U512(le_bytes_to_int(as_bytes, False))

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 512) - 1

    #endregion
