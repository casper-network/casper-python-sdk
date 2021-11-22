import datetime

from pycspr.types import Timestamp


def from_bytes(value: bytes) -> Timestamp:
    raise NotImplementedError()
    

def from_json(entity: dict) -> Timestamp:
    # Strip trailing TZ offset - TODO review.
    if obj.endswith("Z"):
        obj = obj[:-1]
        obj = f"{obj}+00:00"

    return datetime.datetime.fromisoformat(obj).timestamp()


def to_bytes(entity: Timestamp) -> bytes:
    raise NotImplementedError()


def to_json(entity: Timestamp) -> str:
    # Node accepts ISO millisecond precise UTC timestamps.
    ts_3_decimal_places = round(entity, 3)
    ts_datetime = datetime.datetime.fromtimestamp(
        ts_3_decimal_places,
        tz=datetime.timezone.utc
        )
    ts_iso = ts_datetime.isoformat()

    return f"{ts_iso[:-9]}Z"
