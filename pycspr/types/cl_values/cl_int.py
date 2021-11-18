import dataclasses

from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_I32(CL_Value):
    """Represents a CL type value: I32.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_I64(CL_Value):
    """Represents a CL type value: I64.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_U8(CL_Value):
    """Represents a CL type value: U8.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 8) - 1


@dataclasses.dataclass
class CL_U32(CL_Value):
    """Represents a CL type value: U32.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 32) - 1


@dataclasses.dataclass
class CL_U64(CL_Value):
    """Represents a CL type value: U64.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 64) - 1


@dataclasses.dataclass
class CL_U128(CL_Value):
    """Represents a CL type value: U128.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 128) - 1


@dataclasses.dataclass
class CL_U256(CL_Value):
    """Represents a CL type value: U256.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 256) - 1


@dataclasses.dataclass
class CL_U512(CL_Value):
    """Represents a CL type value: U512.
    
    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 512) - 1
