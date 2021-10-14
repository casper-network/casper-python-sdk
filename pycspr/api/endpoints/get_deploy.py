import typing

from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection, deploy_id: typing.Union[bytes, str]) -> dict:
    """Returns on-chain deploy information.

    :param node: Information required to connect to a node.
    :param deploy_id: Identifier of a processed deploy.

    :returns: On-chain deploy information.

    """
    def _get_params(deploy_id: typing.Union[bytes, str]) -> dict:
        return {
            "deploy_hash": deploy_id.hex() if isinstance(deploy_id, bytes) else deploy_id
        }

    return node.get_rpc_response(
        constants.RPC_INFO_GET_DEPLOY,
        get_params(deploy_id)
        )

