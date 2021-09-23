import typing

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
    params = get_params(deploy)
    response = node.get_response(constants.RPC_ACCOUNT_PUT_DEPLOY, params)

    return response["deploy_hash"]


def get_params(deploy: Deploy) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy: A deploy to be dispatched to a node.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "deploy": encode_deploy(deploy)
    }
