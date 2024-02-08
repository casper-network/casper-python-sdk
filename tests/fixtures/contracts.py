import os
import pathlib

import pytest


_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"


@pytest.fixture(scope="session")
def path_to_wasm_auction_bid() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "add_bid.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_auction_bid_withdrawal() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "withdraw_bid.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_delegate() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "delegate.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_delegate_withdrawal() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "undelegate.wasm"
