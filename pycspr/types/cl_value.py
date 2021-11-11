import dataclasses

from pycspr.types.cl_type import CLType


@dataclasses.dataclass
class CLValue():
    """A CL value mapped from python type system.

    """
    # Type information used by a deserializer.
    cl_type: CLType

    # Parsed pythonic representation of underlying data (for human convenience only).
    parsed: object

    # Byte array representation of underlying data.
    bytes: bytes = None

    def __eq__(self, other):
        """Instance equality comparison.

        """
        return self.parsed == other.parsed
