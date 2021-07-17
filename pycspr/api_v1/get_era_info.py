import typing

import jsonrpcclient as rpc_client

from pycspr.types import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "chain_get_era_info_by_switch_block"


def execute(
    connection_info: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None,
    parse_response: bool = True,
    ) -> dict:
    """Returns current era information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finialised block.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Era information.

    """
    # Get latest.
    if isinstance(block_id, type(None)):
        response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT)

    # Get by hash - bytes.
    elif isinstance(block_id, bytes):
        response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, 
            block_identifier={
                "Hash": block_id.hex()
            }
        )

    # Get by hash - hex.
    elif isinstance(block_id, str):
        response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, 
            block_identifier={
                "Hash": block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT, 
            block_identifier={
                "Height": block_id
            }
        )    

    return response.data.result["era_summary"] if parse_response else response.data.result
