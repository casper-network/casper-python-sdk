# Millisecond durations of relevance.
_MS_1_SECOND: int = 1000
_MS_1_MINUTE: int = 60 * _MS_1_SECOND
_MS_1_HOUR: int = 60 * _MS_1_MINUTE


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
    if interval.endswith("msec"):
        return int(interval[0:-4])

    if interval.endswith("seconds"):
        return int(interval[0:-7]) * _MS_1_SECOND
    if interval.endswith("second"):
        return int(interval[0:-6]) * _MS_1_SECOND
    if interval.endswith("sec"):
        return int(interval[0:-3]) * _MS_1_SECOND

    if interval.endswith("minutes"):
        return int(interval[0:-7]) * _MS_1_MINUTE
    if interval.endswith("minute"):
        return int(interval[0:-6]) * _MS_1_MINUTE
    if interval.endswith("min"):
        return int(interval[0:-3]) * _MS_1_MINUTE
    if interval.endswith("m"):
        return int(interval[0:-1]) * _MS_1_MINUTE

    if interval.endswith("hours"):
        return int(interval[0:-5]) * _MS_1_HOUR
    if interval.endswith("hour"):
        return int(interval[0:-4]) * _MS_1_HOUR
    if interval.endswith("hr"):
        return int(interval[0:-2]) * _MS_1_HOUR
    if interval.endswith("h"):
        return int(interval[0:-1]) * _MS_1_HOUR

    if interval.endswith("s"):
        return int(interval[0:-1]) * _MS_1_SECOND

    raise ValueError("Unsupported humanized time interval")


def milliseconds_to_humanized_time_interval(interval: int) -> int:
    """Converts a human readable time interval to milliseconds.

    :param interval: A human readable time interval.
    :returns: Time interval in milliseconds.

    """
    for typeof, timespan in (
        ("hours", _MS_1_HOUR),
        ("minutes", _MS_1_MINUTE),
        ("seconds", _MS_1_SECOND),
        ("ms", 1),
    ):
        if interval % timespan == 0:
            return f"{int(interval / timespan)}{typeof}"

    raise ValueError("Unsupported humanized time interval")
