import typing

import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> str:
    """Returns an on-chain state root hash at specified block.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: State root hash at specified block.

    """
    # Get latest.
    if isinstance(block_id, type(None)):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_CHAIN_GET_STATE_ROOT_HASH
            )

    # Get by hash - bytes | hex.
    elif isinstance(block_id, (bytes, str)):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_CHAIN_GET_STATE_ROOT_HASH, 
            block_identifier={
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = rpc_client.request(
            connection_info.address_rpc, 
            constants.RPC_CHAIN_GET_STATE_ROOT_HASH, 
            block_identifier={
                "Height": block_id
            }
        )

    return response.data.result["state_root_hash"]
