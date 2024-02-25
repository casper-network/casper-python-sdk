from pycspr.api import constants
from pycspr.api.rpc.endpoints.utils import get_block_id
from pycspr.api.rpc.endpoints.utils import get_account_key
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import AccountID
from pycspr.types import BlockID


def exec(proxy: Proxy, account_id: AccountID, block_id: BlockID = None) -> dict:
    """Returns account information at a certain global state root hash.

    :param proxy: Remote RPC server proxy.
    :param account_id: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Account information in JSON format.

    """
    params: dict = get_account_key(account_id) | get_block_id(block_id)
    response: dict = proxy.get_response(constants.RPC_STATE_GET_ACCOUNT_INFO, params)

    return response["account"]
