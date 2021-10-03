from pycspr.api.constants import RPC_ACCOUNT_PUT_DEPLOY
from pycspr.serialisation.json.encoder.deploy import encode_deploy
from pycspr.types import Deploy

"""Dispatches a deploy to a node for processing.

:param node: Information required to connect to a node.
:param deploy: A deploy to be dispatched to a node.
:returns: Hash of dispatched deploy.
"""


def get_rpc_name():
    return RPC_ACCOUNT_PUT_DEPLOY


def extract_result(response):
    return response["deploy_hash"]


def get_params(deploy: Deploy) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy: A deploy to be dispatched to a node.
    :returns: Parameters to be passed to JSON-RPC API.
    """
    return {
        "deploy": encode_deploy(deploy)
    }
