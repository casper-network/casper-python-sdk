# Millisecond durations of relevance.
_MS_1_DAY: int = 24 * 60 * 60 * 1000
_MS_1_HOUR: int = 60 * 60 * 1000
_MS_1_MINUTE: int = 60 * 1000
_MS_1_SECOND: int = 1000


def humanized_time_interval_to_milliseconds(interval: str) -> int:
    """Converts a human readable time interval to milliseconds.

    :param interval: A human readable time interval.
    :returns: Time interval in milliseconds.

    """
    interval = interval.lower()
    try:
        int(interval)
    except ValueError:
        ...
    else:
        return int(interval)

    if interval.endswith("ms"):
        return int(interval[0:-2])
    if interval.endswith("s"):
        return int(interval[0:-1]) * _MS_1_SECOND
    if interval.endswith("m"):
        return int(interval[0:-1]) * _MS_1_MINUTE
    if interval.endswith("h"):
        return int(interval[0:-1]) * _MS_1_HOUR
    if interval.endswith("day"):
        return int(interval[0:-3]) * _MS_1_DAY

    raise ValueError("Unsupported humanized time interval")


def milliseconds_to_humanized_time_interval(interval: int) -> int:
    """Converts a human readable time interval to milliseconds.

    :param interval: A human readable time interval.
    :returns: Time interval in milliseconds.

    """
    for typeof, timespan in (
        ("day", _MS_1_DAY),
        ("h", _MS_1_HOUR),
        ("m", _MS_1_MINUTE),
        ("s", _MS_1_SECOND),
        ("ms", 1),
    ):
        if interval % timespan == 0:
            return f"{int(interval / timespan)}{typeof}"

    raise ValueError("Unsupported humanized time interval")
