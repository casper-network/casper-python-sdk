from typing import Union
from pycspr.api.constants import RPC_INFO_GET_DEPLOY

"""
Returns on-chain deploy information.

:param node: Information required to connect to a node.
:param deploy_id: Identifier of a processed deploy.

:returns: On-chain deploy information.
"""


def get_rpc_name():
    return RPC_INFO_GET_DEPLOY


def extrac_result(response):
    return response


def get_params(deploy_id: Union[bytes, str]) -> dict:
    """
    Returns JSON-RPC API request parameters.

    :param deploy_id: Identifier of a queued/processed deploy.
    :returns: Parameters to be passed to JSON-RPC API.
    """
    return {
        "deploy_hash": deploy_id.hex()
        if isinstance(deploy_id, bytes) else deploy_id
    }
