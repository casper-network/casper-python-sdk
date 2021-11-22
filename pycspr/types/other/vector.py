import dataclasses
import typing

from pycspr.types.cl import cl_values


@dataclasses.dataclass
class Vector():
    # Associated vector.
    vec: typing.List[bytes]
