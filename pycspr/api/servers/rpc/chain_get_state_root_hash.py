from pycspr import types
from pycspr.api import constants
from pycspr.api import params as params_factory
from pycspr.api.servers.rpc.utils import Proxy


def exec(
    proxy: Proxy,
    block_id: types.BlockID = None
) -> types.StateRootHash:
    """Returns root hash of global state at a finalised block.

    :param block_id: Identifier of a finalised block.
    :returns: State root hash at finalised block.

    """
    response = proxy.get_response(
        constants.RPC_CHAIN_GET_STATE_ROOT_HASH,
        params_factory.get_state_root_hash_params(block_id)
        )

    return bytes.fromhex(response["state_root_hash"])
