from pycspr.types import DeployID
from pycspr.api import constants
from pycspr.api.servers.rpc import utils
from pycspr.api.servers.rpc.utils import Proxy


def exec(proxy: Proxy, deploy_id: DeployID) -> dict:
    """Returns on-chain deploy information.

    :param proxy: Remote RPC server proxy. 
    :param deploy_id: Identifier of a deploy processed by network.
    :returns: On-chain deploy information.

    """
    params: dict = utils.get_deploy_id(deploy_id)
    response: dict = proxy.get_response(constants.RPC_INFO_GET_DEPLOY, params)

    return response["deploy"]
