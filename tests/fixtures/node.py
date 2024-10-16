import os
import random

import pytest

import pycspr


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


@pytest.fixture()
def REQUEST_ID() -> int:
    return 0
    return random.randint(0, int(1e2))


@pytest.fixture()
def REQUEST_ID_STATIC() -> int:
    return 0
