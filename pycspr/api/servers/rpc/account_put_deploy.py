from pycspr import serialisation
from pycspr.api import constants
from pycspr.api.servers.rpc.utils import Proxy
from pycspr.types import Deploy


def exec(proxy: Proxy, deploy: Deploy) -> bytes:
    """Dispatches a deploy to a node for processing.

    :param proxy: Remote RPC server proxy. 
    :param deploy: A deploy to be processed at a node.

    """    
    response: dict = proxy.get_response(constants.RPC_ACCOUNT_PUT_DEPLOY, {
        "deploy": serialisation.to_json(deploy)
    })

    return response["deploy_hash"]
