import pytest

import pycctl


@pytest.mark.asyncio
async def test_that_cctl_assets_exist() -> None:
    pycctl.validator.validate_infra_net_assets_setup()


@pytest.mark.asyncio
async def test_that_cctl_network_is_up() -> None:
    pycctl.validator.validate_infra_net_is_up()


@pytest.mark.asyncio
async def test_that_cctl_accounts_are_funded() -> None:
    pycctl.validator.validate_chain_accounts_are_funded()
