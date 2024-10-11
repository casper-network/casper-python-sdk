import dataclasses
import typing


U8 = typing.NewType(
    "Unsigned 8 bit integer.", int
)

U16 = typing.NewType(
    "Unsigned 16 bit integer.", int
)

U32 = typing.NewType(
    "Unsigned 32 bit integer.", int
)

U64 = typing.NewType(
    "Unsigned 64 bit integer.", int
)

U128 = typing.NewType(
    "Unsigned 128 bit integer.", int
)

U256 = typing.NewType(
    "Unsigned 256 bit integer.", int
)

U512 = typing.NewType(
    "Unsigned 512 bit integer.", int
)

@dataclasses.dataclass
class TimeDifference():
    """A span of time during which a set of system events may or may not occur.

    """
    # Time difference as the number of milliseconds since the Unix epoch.
    value: int


@dataclasses.dataclass
class Timestamp():
    """Timestamp pertaining to a moment in time upon which some form of system event occurred.

    """
    # Milliseconds since epoch ... ie unix time.
    value: float
