import json
import typing

from jsonrpcclient import parse, request
import requests

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo
from pycspr.serialisation.json.encoder.deploy import encode_deploy
from pycspr.types import Deploy



def execute(node: NodeConnectionInfo, deploy: Deploy) -> str:
    """Dispatches a deploy to a node for processing.

    :param node: Information required to connect to a node.
    :param deploy: A deploy to be dispatched to a node.
    :returns: Hash of dispatched deploy.

    """
    response = requests.post(
        node.address_rpc,
        json=request(constants.RPC_ACCOUNT_PUT_DEPLOY,
            {"deploy":encode_deploy(deploy)})
        )

    return parse(response.json()).result["deploy_hash"]
