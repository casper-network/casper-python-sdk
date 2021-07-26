import typing

from pycspr import crypto
from pycspr import factory
from pycspr import types
from pycspr.client import NodeConnectionInfo
from pycspr.api.get_account_info import execute as get_account_info



def execute(
    connection_info: NodeConnectionInfo,
    account_key: bytes,
    state_root_hash: typing.Union[bytes, None] = None,
    ) -> types.UnforgeableReference:
    """Returns an on-chain account's main purse unforgeable reference.

    :param connection_info: Information required to connect to a node.
    :param account_key: Key of an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Account main purse unforgeable reference.

    """
    # Map account key to an account hash.
    account_hash = crypto.get_account_hash(account_key)

    # Query node for account info.
    account_info = get_account_info(connection_info, account_hash, state_root_hash)

    # Decode uref.
    return factory.create_uref_from_string(account_info["main_purse"])
