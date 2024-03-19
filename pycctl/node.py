from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rest import Client as RestClient
from pycspr.api.rpc import Client as RpcClient
from pycspr.api.rpc_speculative import Client as RpcSpeculativeClient
from pycspr.api.sse import Client as SseClient
from pycctl.constants import BASE_PORT_REST
from pycctl.constants import BASE_PORT_RPC
from pycctl.constants import BASE_PORT_SPEC_EXEC
from pycctl.constants import BASE_PORT_SSE
from pycctl.types import NodePortType


_PORT_BY_TYPE = {
    NodePortType.REST: BASE_PORT_REST,
    NodePortType.RPC: BASE_PORT_RPC,
    NodePortType.RPC_SPECULATIVE: BASE_PORT_SPEC_EXEC,
    NodePortType.SSE: BASE_PORT_SSE,
}


def get_port(typeof: NodePortType, node_idx: int) -> int:
    return _PORT_BY_TYPE[typeof] + node_idx


def get_rest_client(node_idx: int = 1) -> RestClient:
    return RestClient(
        NodeConnectionInfo(
            port_rest=get_port(NodePortType.REST, node_idx),
        )
    )


def get_rpc_client(node_idx: int = 1) -> RpcClient:
    return RpcClient(
        NodeConnectionInfo(
            port_rpc=get_port(NodePortType.RPC, node_idx),
        )
    )


def get_rpc_speculative_client(node_idx: int = 1) -> RpcSpeculativeClient:
    return RpcSpeculativeClient(
        NodeConnectionInfo(
            port_rpc_speculative=get_port(NodePortType.RPC_SPECULATIVE, node_idx),
        )
    )


def get_sse_client(node_idx: int = 1) -> SseClient:
    return SseClient(
        NodeConnectionInfo(
            port_rpc=get_port(NodePortType.RPC, node_idx),
            port_sse=get_port(NodePortType.SSE, node_idx),
        )
    )

