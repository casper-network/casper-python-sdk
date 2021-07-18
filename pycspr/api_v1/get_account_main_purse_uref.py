import typing

from pycspr import crypto
from pycspr.api_v1.get_account_info import execute as get_account_info
from pycspr.client.connection_info import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    account_key: bytes,
    state_root_hash: typing.Union[bytes, None] = None,
    ) -> str:
    """Returns an on-chain account's main purse unforgeable reference.

    :param connection_info: Information required to connect to a node.
    :param account_key: Key of an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Account main purse unforgeable reference.

    """
    account_hash = crypto.get_account_hash(account_key)
    account_info = get_account_info(connection_info, account_hash, state_root_hash)
    
    return account_info["main_purse"]
