import typing

import jsonrpcclient as rpc_client

import pycspr
from pycspr.types import Deploy



# Method upon client to be invoked.
_API_ENDPOINT = "account_put_deploy"


def execute(
    deploy: Deploy,
    parse_response: bool = True,
    ) -> typing.Union[dict, str]:
    """Dispatches a deploy to a node for processing.

    :param block_id: Identifier of a finialised block.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: State root hash at specified block.

    """
    # TODO: validate inputs: null, ttl, timestamp
    
    raise NotImplementedError()
