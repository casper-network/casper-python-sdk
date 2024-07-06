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
def NODE_BINARY_CLIENT(
    NODE_BINARY_CONNECTION_INFO: pycspr.NodeBinaryConnectionInfo
) -> pycspr.NodeBinaryClient:
    return pycspr.NodeBinaryClient(NODE_BINARY_CONNECTION_INFO)

@pytest.fixture(scope="session")
def NODE_BINARY_CONNECTION_INFO(
    NODE_HOST: str,
    NODE_BINARY_PORT: int
) -> pycspr.NodeBinaryConnectionInfo:
    return pycspr.NodeBinaryConnectionInfo(
        "2.0.0",
        NODE_HOST,
        NODE_BINARY_PORT
    )


@pytest.fixture(scope="session")
def NODE_BINARY_PORT() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_BINARY_PORT", 12101))


@pytest.fixture(scope="session")
def NODE_HOST() -> str:
    return os.getenv("PYCSPR_TEST_NODE_HOST", "localhost")


@pytest.fixture(scope="session")
def NODE_REST_CLIENT(
    NODE_REST_CONNECTION_INFO: pycspr.NodeRestConnectionInfo
) -> pycspr.NodeRestClient:
    return pycspr.NodeRestClient(NODE_REST_CONNECTION_INFO)


@pytest.fixture(scope="session")
def NODE_REST_CONNECTION_INFO(
    NODE_HOST: str,
    NODE_REST_PORT: int
) -> pycspr.NodeRestConnectionInfo:
    return pycspr.NodeRestConnectionInfo(NODE_HOST, NODE_REST_PORT)


@pytest.fixture(scope="session")
def NODE_REST_PORT() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_REST_PORT", 13101))


@pytest.fixture(scope="session")
def NODE_SSE_CLIENT(
    NODE_SSE_CONNECTION_INFO: pycspr.NodeSseConnectionInfo
) -> pycspr.NodeSseClient:
    return pycspr.NodeSseClient(NODE_SSE_CONNECTION_INFO)


@pytest.fixture(scope="session")
def NODE_SSE_CONNECTION_INFO(
    NODE_HOST: str,
    NODE_SSE_PORT: int
) -> pycspr.NodeSseConnectionInfo:
    return pycspr.NodeSseConnectionInfo(NODE_HOST, NODE_SSE_PORT)


@pytest.fixture(scope="session")
def NODE_SSE_PORT() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_SSE_PORT", 14101))




@pytest.fixture(scope="session")
def PORT_RPC() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_PORT_RPC", 11101))


@pytest.fixture(scope="session")
def PORT_RPC_SPECULATIVE() -> int:
    return int(os.getenv("PYCSPR_TEST_NODE_PORT_RPC_SPECULATIVE", 25101))


@pytest.fixture(scope="session")
def CONNECTION_RPC(NODE_HOST: str, PORT_RPC: int) -> pycspr.NodeRpcConnectionInfo:
    return pycspr.NodeRpcConnectionInfo(NODE_HOST, PORT_RPC)


@pytest.fixture(scope="session")
def CONNECTION_RPC_SPECULATIVE(
    NODE_HOST: str,
    PORT_RPC_SPECULATIVE: int
) -> pycspr.NodeSpeculativeRpcConnectionInfo:
    return pycspr.NodeSpeculativeRpcConnectionInfo(NODE_HOST, PORT_RPC_SPECULATIVE)
