import os
import pathlib

import pytest

import pycspr

_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"


@pytest.fixture(scope="session")
def CLIENT(
    NODE_HOST,
    NODE_PORT_REST,
    NODE_PORT_RPC,
    NODE_PORT_SSE
) -> pycspr.NodeClient:
    return pycspr.NodeClient(pycspr.NodeConnection(
        host=NODE_HOST,
        port_rest=NODE_PORT_REST,
        port_rpc=NODE_PORT_RPC,
        port_sse=NODE_PORT_SSE
    ))


@pytest.fixture(scope="session")
def NODE_HOST() -> str:
    return os.getenv("PYCSPR_TEST_NODE_HOST", "localhost")


@pytest.fixture(scope="session")
def NODE_PORT_REST() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_REST", 14101)


@pytest.fixture(scope="session")
def NODE_PORT_RPC() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_RPC", 11101)


@pytest.fixture(scope="session")
def NODE_PORT_SSE() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_SSE", 18101)
