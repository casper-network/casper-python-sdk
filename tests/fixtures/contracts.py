import os
import pathlib

import pytest


_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"


@pytest.fixture(scope="session")
def path_to_wasm_auction_bid() -> str:
    return _PATH_TO_NCTL_ASSETS / "bin"  / "auction" / "add_bid.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_auction_bid_withdrawal() -> str:
    return _PATH_TO_NCTL_ASSETS / "bin"  / "auction" / "withdraw_bid.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_delegate() -> str:
    return _PATH_TO_NCTL_ASSETS / "bin"  / "auction" / "delegate.wasm"


@pytest.fixture(scope="session")
def path_to_wasm_delegate_withdrawal() -> str:
    return _PATH_TO_NCTL_ASSETS / "bin"  / "auction" / "undelegate.wasm"
