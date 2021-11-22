import dataclasses
import datetime as dt


@dataclasses.dataclass
class Timestamp():
    """A timestamp encodeable as millisecond precise seconds since epoch.

    """
    # Timestamp in milliseconds.
    value: float

    def __eq__(self, other) -> bool:
        return self.value == other.value


    @staticmethod
    def from_string(as_string: str) -> "Timestamp":
        if as_string.endswith("Z"):
            as_string = as_string[:-1]
            as_string = f"{as_string}+00:00"

        return Timestamp(dt.datetime.fromisoformat(as_string).timestamp())


    def to_string(self) -> str:
        ts_3_decimal_places = round(self.value, 3)
        ts_datetime = dt.datetime.fromtimestamp(
            ts_3_decimal_places,
            tz=dt.timezone.utc
            )
        ts_iso = ts_datetime.isoformat()

        return f"{ts_iso[:-9]}Z"
