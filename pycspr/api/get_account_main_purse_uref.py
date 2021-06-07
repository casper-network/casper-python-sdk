from pycspr.api.get_account_info import execute as get_account_info


def execute(
    account_key: str,
    state_root_hash: str = None,
    ) -> str:
    """Returns an on-chain account hash mapped from an account key.

    :param account_key: Key of an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.

    :returns: Account main purse unforgeable reference.

    """
    account_info = get_account_info(account_key, state_root_hash)
    
    return account_info["main_purse"]
