import typing

from jsonrpcclient import parse, request
import requests

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    block_id: typing.Union[None, str, int] = None
    ) -> typing.Tuple[str, list]:
    """Returns on-chain block transfers information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block transfers information.

    """
    # Get latest.
    if isinstance(block_id, type(None)):
        response = requests.post(
            connection_info.address_rpc,
            json=request(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS)
            )

    # Get by hash - bytes | hex.
    elif isinstance(block_id, (bytes, str)):
        response = requests.post(
            connection_info.address_rpc,
            json=request(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS),
            block_identifier={
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = requests.post(
            connection_info.address_rpc,
            json=request(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS),
            block_identifier={
                "Height": block_id
            }
        )
   
    parsed = parse(response.json())
    return (
        parsed.result["block_hash"],
        parsed.result["transfers"],
    )
