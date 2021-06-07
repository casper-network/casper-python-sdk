import typing

import jsonrpcclient as rpc_client

import pycspr



# RPC method to be invoked.
_API_ENDPOINT = "info_get_deploy"


def execute(
    deploy_hash: str,
    parse_response: bool = True,
    ) -> dict:
    """Returns on-chain deploy information.

    :param block_id: Identifier of a finialised block.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: On-chain deploy information.

    """
    response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT, 
        deploy_hash=deploy_hash
    )

    return response.data.result["deploy"] if parse_response else response.data.result
