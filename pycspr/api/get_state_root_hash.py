import typing

import jsonrpcclient as rpc_client

import pycspr



# Method upon client to be invoked.
_API_ENDPOINT = "chain_get_state_root_hash"


def execute(
    block_id: str = None,
    parse_response: bool = True,
    ) -> typing.Union[dict, str]:
    """Returns an on-chain state root hash at specified block.

    :param block_id: Identifier of a finialised block.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: State root hash at specified block.

    """
    response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT,
        block_identifier=block_id,
        )

    return response.data.result["state_root_hash"] if parse_response else response.data.result
