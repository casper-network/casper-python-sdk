import time

import pytest

import pycctl
import pycspr
from pycctl.types import AccountType
from pycspr.api.sidecar.rpc import Client as NodeClient
from pycspr.types.node import Deploy
from pycspr.type_defs.cl_values import CLV_String
from pycspr.type_defs.cl_values import CLV_U8
from pycspr.type_defs.cl_values import CLV_U256
from pycspr.types.node import DeployOfModuleBytes
from pycctl.fsys import get_path_to_account_private_key


_CONTRACT_FNAME = "activate_bid.wasm"
_TOKEN_DECIMALS = 10
_TOKEN_NAME = "Acme Wilderness"
_TOKEN_SUPPLY = int(1e18)
_TOKEN_SYMBOL = "ACME"


async def test_sc_exists():
    assert pycctl.fsys.get_path_to_binary(_CONTRACT_FNAME).exists()


async def test_sc_installation(SIDECAR_RPC_CLIENT: NodeClient):
    # Set installation tx.
    tx: Deploy = await _get_tx()

    # Dispatch tx.
    await _dispatch(SIDECAR_RPC_CLIENT, tx)

    # Install SC
    #   dispatch wasm
    #   await finalisation
    #   assert named keys mutation
    #   assert sc initial state
    #   cache contract version address
    #   cache contract package address
    raise ValueError("dsadsad")


async def _get_tx() -> Deploy:
    sc_binary_path = pycctl.fsys.get_path_to_binary(_CONTRACT_FNAME)

    sc_operator_pvk = pycspr.parse_private_key(
        get_path_to_account_private_key(AccountType.USER)
        )

    tx_params = \
        pycspr.create_deploy_parameters(
            account=sc_operator_pvk,
            chain_name=pycctl.constants.CHAIN_NAME,
            )

    tx_payment = \
        pycspr.create_standard_payment(pycctl.constants.SC_PAYMENT_INSTALL)

    tx_session = \
        DeployOfModuleBytes(
            module_bytes=pycspr.read_wasm(sc_binary_path),
            args={
                "token_decimals": CLV_U8(_TOKEN_DECIMALS),
                "token_name": CLV_String(_TOKEN_NAME),
                "token_symbol": CLV_String(_TOKEN_SYMBOL),
                "token_total_supply": CLV_U256(_TOKEN_SUPPLY),
            }
        )

    tx = pycspr.create_deploy(tx_params, tx_payment, tx_session)

    tx.approve(sc_operator_pvk)

    return tx


async def _dispatch(client: NodeClient, tx: Deploy):
    client.send_deploy(tx)
    while True:
        time.sleep(float(1))
        execution_info = client.get_deploy(tx.hash).execution_info
        print(execution_info)

        break
