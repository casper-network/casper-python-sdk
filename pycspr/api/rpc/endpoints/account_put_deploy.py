from pycspr import serialisation
from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import Deploy
from pycspr.types import DeployID


def exec(proxy: Proxy, deploy: Deploy) -> DeployID:
    """Dispatches a deploy to a node for processing.

    :param proxy: Remote RPC server proxy.
    :param deploy: A deploy to be processed at a node.
    :returns: Deploy identifier.

    """
    response: dict = proxy.get_response(constants.RPC_ACCOUNT_PUT_DEPLOY, {
        "deploy": serialisation.to_json(deploy)
    })

    return response["deploy_hash"]
