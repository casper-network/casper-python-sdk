import typing

import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    deploy_id: typing.Union[bytes, str]
    ) -> dict:
    """Returns on-chain deploy information.

    :param connection_info: Information required to connect to a node.
    :param deploy_id: Identifier of a processed deploy.

    :returns: On-chain deploy information.

    """
    deploy_id = deploy_id.hex() if isinstance(deploy_id, bytes) else deploy_id
    response = rpc_client.request(
        connection_info.address_rpc,
        constants.RPC_INFO_GET_DEPLOY, 
        deploy_hash=deploy_id
    )

    return response.data.result["deploy"]
