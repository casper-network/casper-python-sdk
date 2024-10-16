import datetime

from pycspr.api.node.bin.types.chain import Transaction_V2_Header
from pycspr.api.node.bin.types.primitives import TimeDifference, Timestamp


def get_chain_name() -> str:
    return "cspr-dev-cctl"


def get_timestamp() -> Timestamp:
    return Timestamp(
        value=datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    )


def get_header() -> Transaction_V2_Header:
    raise NotImplementedError()
