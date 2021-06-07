import typing

import jsonrpcclient as rpc_client

import pycspr



# RPC method to be invoked.
_API_ENDPOINT = "chain_get_block_transfers"


def execute(
    block_id: typing.Union[None, str, int] = None,
    parse_response: bool = True,
    ) -> dict:
    """Returns on-chain block transfers information.

    :param block_id: Identifier of a finialised block.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: On-chain block transfers information.

    """
    # Get latest.
    if isinstance(block_id, type(None)):
        response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT)

    # Get by hash.
    elif isinstance(block_id, str):
        response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT, 
            block_identifier={
                "Hash": block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT, 
            block_identifier={
                "Height": block_id
            }
        )

    return response.data.result["block"] if parse_response else response.data.result
