import typing

from pycspr.api.get_rpc_schema import execute as get_rpc_schema
from pycspr.client import NodeConnectionInfo



def execute(node: NodeConnectionInfo, endpoint: str) -> typing.Union[dict, list]:
    """Returns RPC schema for a single endpoint.

    :param node: Information required to connect to a node.
    :param endpoint: A specific endpoint of interest.
    :returns: JSON-RPC schema endpoint fragment.

    """
    schema = get_rpc_schema(node)
    for obj in schema["methods"]:
        if obj["name"].lower() == endpoint.lower():
            return obj
