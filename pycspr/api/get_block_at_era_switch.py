import time

from pycspr.api.get_block import execute as get_block
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    polling_interval_seconds: float = 1.0,
    max_polling_time_seconds: float = 120.0
    ) -> dict:
    """Returns last finalised block in current era.

    :param connection_info: Information required to connect to a node.
    :param polling_interval_seconds: Time interval time (in seconds) before polling for next switch block.
    :param max_polling_time_seconds: Maximum time in seconds to poll.

    :returns: On-chain block information.

    """
    elapsed = 0.0
    while True:
        block = get_block(connection_info)
        if block["header"]["era_end"] is not None:
            return block

        elapsed += polling_interval_seconds
        if elapsed > max_polling_time_seconds:
            break
        time.sleep(polling_interval_seconds)
