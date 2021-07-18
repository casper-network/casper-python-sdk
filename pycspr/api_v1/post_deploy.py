import json
import typing

import jsonrpcclient
import jsonrpcclient as rpc_client

from pycspr.types import Deploy
from pycspr.client.connection_info import NodeConnectionInfo
from pycspr.codec import to_json



# Method upon client to be invoked.
_API_ENDPOINT = "account_put_deploy"


def execute(connection_info: NodeConnectionInfo, deploy: Deploy) -> typing.Union[dict, str]:
    """Dispatches a deploy to a node for processing.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finialised block.
    :returns: State root hash at specified block.

    """
    print(to_json(deploy))

    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, 
        deploy=json.loads(to_json(deploy))
        )

    return response.data.result["deploy_hash"]
