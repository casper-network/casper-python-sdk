from pycspr.types import AccountID
from pycspr.types import BlockID
from pycspr.api import constants
from pycspr.api.servers.rpc import utils
from pycspr.api.servers.rpc.utils import Proxy


def exec(proxy: Proxy, account_id: AccountID, block_id: BlockID = None) -> dict:
    """Returns account information at a certain global state root hash.

    :param proxy: Remote RPC server proxy.
    :param account_id: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Account information in JSON format.

    """    
    params: dict = utils.get_account_key(account_id) | utils.get_block_id(block_id)
    response: dict = proxy.get_response(constants.RPC_STATE_GET_ACCOUNT_INFO, params)

    return response["account"]
