import typing

import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    account_key: bytes,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain account information at a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param account_key: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Account information in JSON format.

    """    
    # Get latest.
    if isinstance(block_id, type(None)):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_STATE_GET_ACCOUNT_INFO,
            public_key=account_key.hex(),
            )

    # Get by hash - bytes | hex.
    elif isinstance(block_id, (bytes, str)):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_STATE_GET_ACCOUNT_INFO, 
            public_key=account_key.hex(),
            block_identifier={
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = rpc_client.request(
            connection_info.address_rpc,
            constants.RPC_STATE_GET_ACCOUNT_INFO, 
            public_key=account_key.hex(),
            block_identifier={
                "Height": block_id
            }
        )
    
    return response.data.result["account"]
