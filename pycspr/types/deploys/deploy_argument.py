import dataclasses

from pycspr.types.cl.cl_values import CL_Value
from pycspr.types.cl.cl_values import CL_String
from pycspr.types.other.u8_array import U8Array


@dataclasses.dataclass
class DeployArgument():
    """An argument to be passed to vm for execution.

    """
    # Argument name mapped to an entry point parameter.
    name: str

    # Argument cl type system value.
    value: CL_Value

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.value == other.value

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "DeployArgument":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return \
            CL_String(self.name).to_bytes() + \
            U8Array(self.value).to_bytes() + \
            self.value.cl_type.to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "DeployArgument":
        return DeployArgument(
            name=obj[0],
            value=CL_Value.from_json(obj[1])
            )

    def to_json(self) -> str:
        return [
            self.name,
            self.value.to_json()
        ]

    #endregion
