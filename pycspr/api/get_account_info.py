from pycspr.crypto import get_account_hash
from pycspr.api.get_account_info_by_account_hash import execute as get_account_info_by_account_hash



def execute(
    account_key: str,
    state_root_hash=None,
    parse_response: bool = True,
    ) -> dict:
    """api account information at a certain state root hash.

    :param account_key: Key of an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Account information in JSON format.

    """
    return get_account_info_by_account_hash(
        get_account_hash(account_key),
        state_root_hash,
        parse_response
    )
