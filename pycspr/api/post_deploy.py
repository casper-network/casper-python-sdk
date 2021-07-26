import json
import typing

import jsonrpcclient as rpc_client

from pycspr import serialisation
from pycspr.types import Deploy
from pycspr.client import NodeConnectionInfo



# Method upon client to be invoked.
_API_ENDPOINT = "account_put_deploy"


def execute(connection_info: NodeConnectionInfo, deploy: Deploy) -> typing.Union[dict, str]:
    """Dispatches a deploy to a node for processing.

    :param connection_info: Information required to connect to a node.
    :param deploy: A deploy to be dispatched to a node.
    :returns: Hash of dispatched deploy.

    """
    # TODO: serialisation.to_dict directly
    deploy = json.loads(serialisation.to_json(deploy))
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, deploy=deploy)

    return response.data.result["deploy_hash"]
