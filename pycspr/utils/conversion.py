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
        return int(interval[0:-1]) * (1000)
    if interval.endswith("m"):
        return int(interval[0:-1]) * (60 * 1000)
    if interval.endswith("h"):
        return int(interval[0:-1]) * (60 * 60 * 1000)
    if interval.endswith("day"):
        return int(interval[0:-3]) * (24 * 60 * 60 * 1000)

    raise ValueError("Unsupported humanized time interval")
