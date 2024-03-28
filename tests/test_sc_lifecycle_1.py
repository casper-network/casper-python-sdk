import pycctl


async def test_that_cctl_assets_exist() -> None:
    pycctl.validator.validate_infra_net_assets_setup()


async def test_that_cctl_network_is_up() -> None:
    await pycctl.validator.validate_infra_net_is_up()


async def test_that_cctl_accounts_are_funded() -> None:
    await pycctl.validator.validate_chain_accounts_are_funded()
