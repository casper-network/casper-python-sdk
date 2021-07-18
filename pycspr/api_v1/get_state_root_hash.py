import typing

import jsonrpcclient as rpc_client

from pycspr.client.connection_info import NodeConnectionInfo



# Method upon client to be invoked.
_API_ENDPOINT = "chain_get_state_root_hash"


def execute(connection_info: NodeConnectionInfo, block_id: typing.Union[None, str, int] = None) -> typing.Union[dict, str]:
    """Returns an on-chain state root hash at specified block.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finialised block.
    :returns: State root hash at specified block.

    """
    response = rpc_client.request(
        connection_info.address_rpc,
        _API_ENDPOINT,
        block_identifier=block_id,
        )

    return response.data.result["state_root_hash"]