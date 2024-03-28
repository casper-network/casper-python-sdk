import os

import pytest

import pycspr


@pytest.fixture(scope="session")
def RPC_CLIENT(CONNECTION_RPC: pycspr.NodeRpcConnectionInfo) -> pycspr.NodeRpcClient:
    return pycspr.NodeRpcClient(CONNECTION_RPC)


@pytest.fixture(scope="session")
def SPECULATIVE_RPC_CLIENT(
    CONNECTION_RPC_SPECULATIVE: pycspr.NodeSpeculativeRpcConnectionInfo
) -> pycspr.NodeSpeculativeRpcClient:
    return pycspr.NodeSpeculativeRpcClient(CONNECTION_RPC_SPECULATIVE)


@pytest.fixture(scope="session")
def REST_CLIENT(
    CONNECTION_REST: pycspr.NodeRestConnectionInfo
) -> pycspr.NodeRestClient:
    return pycspr.NodeRestClient(CONNECTION_REST)


@pytest.fixture(scope="session")
def SSE_CLIENT(CONNECTION_SSE: pycspr.NodeSseConnectionInfo) -> pycspr.NodeSseClient:
    return pycspr.NodeSseClient(CONNECTION_SSE)


@pytest.fixture(scope="session")
def NODE_HOST() -> str:
    return os.getenv("PYCSPR_TEST_NODE_HOST", "localhost")


@pytest.fixture(scope="session")
def PORT_REST() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_PORT_REST", 14101))


@pytest.fixture(scope="session")
def PORT_RPC() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_PORT_RPC", 11101))


@pytest.fixture(scope="session")
def PORT_RPC_SPECULATIVE() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_PORT_RPC_SPECULATIVE", 25101))


@pytest.fixture(scope="session")
def PORT_SSE() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_PORT_SSE", 18101))


@pytest.fixture(scope="session")
def CONNECTION_REST(NODE_HOST: str, PORT_REST: int) -> pycspr.NodeRestConnectionInfo:
    return pycspr.NodeRestConnectionInfo(NODE_HOST, PORT_REST)


@pytest.fixture(scope="session")
def CONNECTION_RPC(NODE_HOST: str, PORT_RPC: int) -> pycspr.NodeRpcConnectionInfo:
    return pycspr.NodeRpcConnectionInfo(NODE_HOST, PORT_RPC)


@pytest.fixture(scope="session")
def CONNECTION_RPC_SPECULATIVE(
    NODE_HOST: str,
    PORT_RPC_SPECULATIVE: int
) -> pycspr.NodeSpeculativeRpcConnectionInfo:
    return pycspr.NodeSpeculativeRpcConnectionInfo(NODE_HOST, PORT_RPC_SPECULATIVE)


@pytest.fixture(scope="session")
def CONNECTION_SSE(NODE_HOST: str, PORT_SSE: int, PORT_RPC: int) -> pycspr.NodeSseConnectionInfo:
    return pycspr.NodeSseConnectionInfo(NODE_HOST, PORT_SSE, PORT_RPC)
