import datetime as dt

from pycspr.type_defs.primitives import TimeDifference, Timestamp


class TimeDifference_Builder():
    """Builder: time difference.

    """
    def __init__(self):
        self.delta: int = None

    def set_delta(self, value: int):
        assert isinstance(value, int)
        self.delta = value
        return self

    def build(self) -> "TimeDifference":
        return TimeDifference(value=self.delta)


class Timestamp_Builder():
    """Builder: timestamp.

    """
    def __init__(self):
        self.ts = dt.datetime.now(tz=dt.timezone.utc).timestamp()

    def set_ts(self, value: float):
        assert isinstance(value, float)
        self.ts = value
        return self

    def build(self) -> Timestamp:
        return Timestamp(value=self.ts)
