import typing

from jsonrpcclient import parse, request
import requests

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
    deploy_id = deploy_id.hex() if isinstance(deploy_id, bytes) else deploy_id
    response = requests.post(
        node.address_rpc,
        json=request(constants.RPC_INFO_GET_DEPLOY,
        {"deploy_hash":deploy_id})
    )

    return parse(response.json()).result["deploy"]
