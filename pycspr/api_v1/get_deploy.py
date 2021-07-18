import typing

import jsonrpcclient as rpc_client

from pycspr.client.connection_info import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "info_get_deploy"


def execute(connection_info: NodeConnectionInfo, deploy_hash: str) -> dict:
    """Returns on-chain deploy information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finialised block.

    :returns: On-chain deploy information.

    """
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, 
        deploy_hash=deploy_hash
    )

    return response.data.result["deploy"]
