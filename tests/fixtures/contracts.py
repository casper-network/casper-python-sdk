import os
import pathlib

import pytest


_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"


@pytest.fixture(scope="session")
def path_to_wasm_auction_bid() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "wasm" / "add_bid.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_auction_bid_withdrawal() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "wasm" / "withdraw_bid.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_delegate() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "wasm" / "delegate.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_delegate_withdrawal() -> str:
    return _PATH_TO_CCTL_ASSETS / "bin" / "wasm" / "undelegate.wasm"
