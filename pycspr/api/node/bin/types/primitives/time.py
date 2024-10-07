import dataclasses


@dataclasses.dataclass
class Timestamp():
    """Timestamp pertaining to a moment in time upon which some form of system event occurred.

    """
    # Milliseconds since epoch ... ie unix time.
    value: float


@dataclasses.dataclass
class TimeDifference():
    """A span of time during which a set of system events may or may not occur.

    """
    # Time difference as the number of milliseconds since the Unix epoch.
    value: int
