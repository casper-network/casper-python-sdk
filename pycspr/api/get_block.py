import typing

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain block information.

    :param node: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block information.

    """
    # Get latest | by hash | by height.
    if isinstance(block_id, type(None)):
        params = None
    elif isinstance(block_id, (bytes, str)):
        params = {
            "block_identifier": {
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }
        }
    elif isinstance(block_id, int):
        params = {
            "block_identifier": {
                "Height": block_id
            }
        }

    response = node.get_response(constants.RPC_CHAIN_GET_BLOCK, params)

    return response["block"]
