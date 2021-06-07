import jsonrpcclient as rpc_client

import pycspr



# RPC method to be invoked.
_API_ENDPOINT = "rpc.discover"


def execute(
    parse_response: bool = True,
    ) -> dict:
    """Returns RPC schema.

    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Node RPC API schema.

    """
    response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT)

    return response.data.result["schema"] if parse_response else response.data.result
