import json
import typing

import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo
from pycspr.serialisation.json.encoder.deploy import encode_deploy
from pycspr.types import Deploy



def execute(connection_info: NodeConnectionInfo, deploy: Deploy) -> str:
    """Dispatches a deploy to a node for processing.

    :param connection_info: Information required to connect to a node.
    :param deploy: A deploy to be dispatched to a node.
    :returns: Hash of dispatched deploy.

    """
    response = rpc_client.request(
        connection_info.address_rpc,
        constants.RPC_ACCOUNT_PUT_DEPLOY,
        deploy=encode_deploy(deploy)
        )

    return response.data.result["deploy_hash"]
