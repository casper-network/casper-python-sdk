import datetime

from pycspr.types.deploy import Timestamp



def encode(entity: Timestamp) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    # NOTE: assume timestamp is UTC millisecond precise.
    timestamp_ms = round(entity, 3)
    timestamp_iso = datetime.datetime.fromtimestamp(timestamp_ms).isoformat()

    return f"{timestamp_iso[:-3]}Z"
