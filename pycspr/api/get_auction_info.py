import typing

import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.api.get_block import execute as get_block
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns current auction system contract information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: Current auction system contract information.

    """
    # Get latest.
    # TODO: verify as a null block should return latest auction infor anyway.
    if isinstance(block_id, type(None)):
        block: dict = get_block(connection_info)
        block_id: str = block["hash"]

    # Get by hash - bytes | hex.
    if isinstance(block_id, (bytes, str)):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_STATE_GET_AUCTION_INFO, 
            block_identifier={
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_STATE_GET_AUCTION_INFO, 
            block_identifier={
                "Height": block_id
            }
        )

    return response.data.result
