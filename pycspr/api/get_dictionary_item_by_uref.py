import typing

import jsonrpcclient as rpc_client

from pycspr import types
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    item_key: str,
    seed_uref: types.UnforgeableReference,
    state_root_hash: typing.Union[bytes, None] = None
    ) -> dict:
    """Returns on-chain block information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: On-chain block information.

    """
    state_root_hash = state_root_hash.hex() if state_root_hash else None

