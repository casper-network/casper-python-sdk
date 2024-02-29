import os

import pytest

import pycspr


@pytest.fixture(scope="session")
def CLIENT(NODE_CONNECTION: pycspr.NodeConnectionInfo) -> pycspr.NodeClient:
    return pycspr.NodeClient(NODE_CONNECTION)


@pytest.fixture(scope="session")
def RPC_CLIENT(NODE_CONNECTION: pycspr.NodeConnectionInfo) -> pycspr.NodeRpcClient:
    return pycspr.NodeRpcClient(NODE_CONNECTION)


@pytest.fixture(scope="session")
def SPECULATIVE_RPC_CLIENT(NODE_CONNECTION: pycspr.NodeConnectionInfo) -> pycspr.NodeSpeculativeRpcClient:
    return pycspr.NodeSpeculativeRpcClient(NODE_CONNECTION)


@pytest.fixture(scope="session")
def REST_CLIENT(NODE_CONNECTION: pycspr.NodeConnectionInfo) -> pycspr.NodeRestClient:
    return pycspr.NodeRestClient(NODE_CONNECTION)


@pytest.fixture(scope="session")
def SSE_CLIENT(NODE_CONNECTION: pycspr.NodeConnectionInfo) -> pycspr.NodeSseClient:
    return pycspr.NodeSseClient(NODE_CONNECTION)


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


@pytest.fixture(scope="session")
def NODE_PORT_SPEC_EXEC() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_SPEC_EXEC", 25101)


@pytest.fixture(scope="session")
def NODE_CONNECTION(
    NODE_HOST,
    NODE_PORT_REST,
    NODE_PORT_RPC,
    NODE_PORT_SSE
) -> pycspr.NodeConnectionInfo:
    return pycspr.NodeConnectionInfo(
        host=NODE_HOST,
        port_rest=NODE_PORT_REST,
        port_rpc=NODE_PORT_RPC,
        port_sse=NODE_PORT_SSE
    )
