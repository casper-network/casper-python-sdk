# Prelude
#   assert wasm exists
#   assert node is up
#   assert test accounts are funded



# Invoke SC by hash 2: users are approved
#   dispatch deploy -> variant = ByContractHash
#   await finalisation
#   query contract state
#   assert contract state

# Invoke SC by hash 3: users transfers tokens
#   dispatch deploy -> variant = ByContractHash
#   await finalisation
#   query contract state
#   assert contract state

import asyncio
import dataclasses
import json
import os
import pathlib
import time

import requests
import pytest

import pycspr
import pycctl
import tests.utils.cctl as cctl

from pycspr import NodeRpcClient


@dataclasses.dataclass
class TestContext():
    __test__ = False

    client: NodeRpcClient = None

    def __init__(self, client: NodeRpcClient):
        self.client = client


async def _test_pre_requisites(ctx: TestContext):

    async def test_net_assets_exist():
        assert cctl.get_evar() is not None
        assert cctl.get_path_to_assets().exists()

    async def test_net_account_keys_exist():
        for account_idx in range(1, cctl.COUNT_OF_USERS + 1):
            assert cctl.get_public_key_of_user(account_idx) is not None
            assert cctl.get_private_key_of_user(account_idx) is not None
        for account_idx in range(1, cctl.COUNT_OF_VALDIATORS + 1):
            assert cctl.get_public_key_of_validator(account_idx) is not None
            assert cctl.get_private_key_of_validator(account_idx) is not None
        assert cctl.get_public_key_of_faucet() is not None
        assert cctl.get_private_key_of_faucet() is not None

    async def test_net_is_up():
        assert ctx.client.get_node_status()["reactor_state"] == "Validate"

    async def test_net_accounts_are_funded():
        for account_idx in range(1, cctl.COUNT_OF_USERS + 1):
            public_key = cctl.get_public_key_of_user(account_idx)
            account_key = public_key.account_key
            purse_id = ctx.client.get_account_main_purse_uref(account_key)
            assert await ctx.client.get_account_balance(purse_id) > 0

        time.sleep(1.0)

    for func in {
        test_net_assets_exist,
        test_net_account_keys_exist,
        test_net_is_up,
        test_net_accounts_are_funded,
    }:
        await func()


async def _test_sc_installation(ctx: TestContext):
    # Install SC
    #   dispatch wasm
    #   await finalisation
    #   assert named keys mutation
    #   assert sc initial state
    #   cache contract version address
    #   cache contract package address
    pass


async def _test_sc_invocation_1(ctx: TestContext):
    # Invoke SC by hash 1: users deposit cspr for token
    #   dispatch deploy -> variant = ByContractHash
    #   await finalisation
    #   query contract state
    #   assert contract state
    pass


async def _test_sc_invocation_2(ctx: TestContext):
    # Invoke SC by hash 2: users are approved
    #   dispatch deploy -> variant = ByContractHash
    #   await finalisation
    #   query contract state
    #   assert contract state
    pass


async def _test_sc_invocation_3(ctx: TestContext):
    # Invoke SC by hash 3: users transfers tokens
    #   dispatch deploy -> variant = ByContractHash
    #   await finalisation
    #   query contract state
    #   assert contract state
    pass


async def test_01(SIDECAR_RPC_CLIENT) -> None:
    ctx = TestContext(SIDECAR_RPC_CLIENT)
    for func in {
        _test_pre_requisites,
        _test_sc_installation,
        _test_sc_invocation_1,
        _test_sc_invocation_2,
        _test_sc_invocation_3,
    }:
        await func(ctx)

    # raise TypeError()
