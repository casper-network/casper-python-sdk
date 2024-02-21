from pycspr.types import BlockID
from pycspr.types import StateRootHash
from pycspr.api.servers.rpc import utils
from pycspr.api.servers.rpc.utils import Proxy


_ENDPOINT: str = "chain_get_state_root_hash"


def exec(proxy: Proxy, block_id: BlockID = None) -> StateRootHash:
    """Returns root hash of global state at a finalised block.

    :param block_id: Identifier of a finalised block.
    :returns: State root hash at finalised block.

    """
    params = utils.get_block_id(block_id)
    response = proxy.get_response(_ENDPOINT, params)

    return bytes.fromhex(response["state_root_hash"])
