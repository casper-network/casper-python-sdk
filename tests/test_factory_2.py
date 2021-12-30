import random

import pycspr
from pycspr.types import Deploy


def test_create_validator_auction_bid(deploy_params, a_test_account, path_to_wasm_auction_bid):
    assert isinstance(pycspr.create_validator_auction_bid(
        params=deploy_params,
        amount=random.randint(0, 1e9),
        delegation_rate=random.randint(0, 20),
        public_key=a_test_account.as_public_key,
        path_to_wasm=path_to_wasm_auction_bid
        ),
        Deploy
        )


def test_create_validator_auction_bid_withdrawal(
    deploy_params,
    a_test_account,
    a_test_uref,
    path_to_wasm_auction_bid_withdrawal
):
    assert isinstance(pycspr.create_validator_auction_bid_withdrawal(
        params=deploy_params,
        amount=random.randint(0, 1e9),
        public_key=a_test_account.as_public_key,
        path_to_wasm=path_to_wasm_auction_bid_withdrawal,
        unbond_purse_ref=a_test_uref
        ),
        Deploy
        )


def test_create_validator_delegate(deploy_params, a_test_account, path_to_wasm_delegate):
    assert isinstance(pycspr.create_validator_delegation(
        params=deploy_params,
        amount=random.randint(0, 1e9),
        public_key_of_delegator=a_test_account.as_public_key,
        public_key_of_validator=a_test_account.as_public_key,
        path_to_wasm=path_to_wasm_delegate
        ),
        Deploy
        )


def test_create_validator_delegate_withdrawal(
    deploy_params,
    a_test_account,
    path_to_wasm_delegate_withdrawal
):
    assert isinstance(pycspr.create_validator_delegation_withdrawal(
        params=deploy_params,
        amount=random.randint(0, 1e9),
        public_key_of_delegator=a_test_account.as_public_key,
        public_key_of_validator=a_test_account.as_public_key,
        path_to_wasm=path_to_wasm_delegate_withdrawal
        ),
        Deploy
        )
