import abc
import dataclasses
import enum
import typing

class CL_TypeKey(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    ANY = 21
    BOOL = 0
    BYTE_ARRAY = 15
    I32 = 1
    I64 = 2
    KEY = 11
    LIST = 14
    MAP = 17
    OPTION = 13
    PUBLIC_KEY = 22
    RESULT = 16
    STRING = 10
    TUPLE_1 = 18
    TUPLE_2 = 19
    TUPLE_3 = 20
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8
    UNIT = 9
    UREF = 12


@dataclasses.dataclass
class CL_Type():
    """Base class encapsulating CL type information associated with a value.

    """
    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key

    @abc.abstractmethod
    def as_bytes(self) -> bytes:
        pass

    @abc.abstractmethod
    def as_json(self) -> typing.Union[str, dict]:
        pass
