import pycspr
from pycspr.types import CL_URef
from pycspr.types import GlobalStateID
from pycspr.types import PurseID
from pycspr.types import PurseIDType

def test_get_account_balance_under_purse_uref(CLIENT, account_main_purse_uref: CL_URef, global_state_id: GlobalStateID):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(
        PurseID(account_main_purse_uref, PurseIDType.UREF),
        global_state_id)
        )


def test_get_account_balance_under_account_hash(CLIENT, account_hash: bytes, global_state_id: GlobalStateID):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(
        PurseID(account_hash, PurseIDType.ACCOUNT_HASH),
        global_state_id)
        )


def test_get_account_balance_under_account_key(CLIENT, account_key: bytes, global_state_id: GlobalStateID):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(
        PurseID(account_key, PurseIDType.PUBLIC_KEY),
        global_state_id)
        )
