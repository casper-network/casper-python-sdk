import typing

from jsonrpcclient import parse, request
import requests

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns current era information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: Era information.

    """
    # Get latest.
    if isinstance(block_id, type(None)):
        response = requests.post(
            connection_info.address_rpc,
            json=request(constants.RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK)
            )

    # Get by hash - bytes | hex.
    elif isinstance(block_id, (bytes, str)):
        response = requests.post(
            connection_info.address_rpc,
            json=request(constants.RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK,
            {"block_identifier":{
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }})
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = requests.post(
            connection_info.address_rpc,
            json=request(constants.RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK,
            {"block_identifier":{
                "Height": block_id
            }})
        )    

    return parse(response.json()).result["era_summary"]
