import typing

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    deploy_id: typing.Union[bytes, str]
    ) -> dict:
    """Returns on-chain deploy information.

    :param node: Information required to connect to a node.
    :param deploy_id: Identifier of a processed deploy.

    :returns: On-chain deploy information.

    """
    params = get_params(deploy_id)
    response = node.get_response(constants.RPC_INFO_GET_DEPLOY, params)

    return response["deploy"]


def get_params(deploy_id: typing.Union[bytes, str]) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy_id: Identifier of a queued/processed deploy.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "deploy_hash": deploy_id.hex() if isinstance(deploy_id, bytes) else deploy_id
    }