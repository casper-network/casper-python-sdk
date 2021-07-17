import json
import typing

import jsonrpcclient as rpc_client

from pycspr.types import Deploy
from pycspr.types import NodeConnectionInfo
from pycspr.codec import to_json



# Method upon client to be invoked.
_API_ENDPOINT = "account_put_deploy"


def execute(connection_info: NodeConnectionInfo, deploy: Deploy, parse_response: bool = True) -> typing.Union[dict, str]:
    """Dispatches a deploy to a node for processing.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finialised block.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: State root hash at specified block.

    """
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, 
        deploy=json.loads(to_json(deploy))
        )

    return response.data.result["deploy_hash"] if parse_response else response.data.result
