import datetime as dt

from pycspr.utils import constants


def humanized_time_interval_from_ms(value: int) -> int:
    for typeof, timespan in (
        ("hours", constants.MS_1_HOUR),
        ("minutes", constants.MS_1_MINUTE),
        ("seconds", constants.MS_1_SECOND),
        ("ms", 1),
    ):
        if value % timespan == 0:
            return f"{int(value / timespan)}{typeof}"

    raise ValueError("Unsupported humanized time interval")


def iso_datetime_from_timestamp(value: float) -> str:
    ts_3_decimal_places = round(value, 3)
    ts_datetime = dt.datetime.fromtimestamp(
        ts_3_decimal_places,
        tz=dt.timezone.utc
        )
    ts_iso = ts_datetime.isoformat()

    return f"{ts_iso[:-9]}Z"


def ms_from_humanized_time_interval(value: str) -> int:
    value = value.lower()
    try:
        int(value)
    except ValueError:
        ...
    else:
        return int(value)

    if value.endswith("ms"):
        return int(value[0:-2])
    if value.endswith("msec"):
        return int(value[0:-4])

    if value.endswith("seconds"):
        return int(value[0:-7]) * constants.MS_1_SECOND
    if value.endswith("second"):
        return int(value[0:-6]) * constants.MS_1_SECOND
    if value.endswith("sec"):
        return int(value[0:-3]) * constants.MS_1_SECOND

    if value.endswith("minutes"):
        return int(value[0:-7]) * constants.MS_1_MINUTE
    if value.endswith("minute"):
        return int(value[0:-6]) * constants.MS_1_MINUTE
    if value.endswith("min"):
        return int(value[0:-3]) * constants.MS_1_MINUTE
    if value.endswith("m"):
        return int(value[0:-1]) * constants.MS_1_MINUTE

    if value.endswith("hours"):
        return int(value[0:-5]) * constants.MS_1_HOUR
    if value.endswith("hour"):
        return int(value[0:-4]) * constants.MS_1_HOUR
    if value.endswith("hr"):
        return int(value[0:-2]) * constants.MS_1_HOUR
    if value.endswith("h"):
        return int(value[0:-1]) * constants.MS_1_HOUR

    if value.endswith("s"):
        return int(value[0:-1]) * constants.MS_1_SECOND

    raise ValueError("Unsupported humanized time interval")


def timestamp_from_iso_datetime(value: str) -> float:
    if value.endswith("Z"):
        value = value[:-1]
        value = f"{value}+00:00"

    return dt.datetime.fromisoformat(value).timestamp()
