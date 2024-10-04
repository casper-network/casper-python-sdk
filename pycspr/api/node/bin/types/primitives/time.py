import dataclasses

@dataclasses.dataclass
class Timestamp():
    # Milliseconds since epoch ... ie unix time.
    value: float
