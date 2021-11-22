import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class DeployArgument():
    """An argument to be passed to vm for execution.

    """
    # Argument name mapped to an entry point parameter.
    name: str

    # Argument cl type system value.
    value: CL_Value

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.name == other.name and \
               self.value == other.value
