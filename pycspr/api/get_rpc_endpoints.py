import typing

from pycspr.api.get_rpc_schema import execute as get_rpc_schema
from pycspr.client import NodeConnectionInfo



def execute(node: NodeConnectionInfo) -> typing.List[str]:
    """Returns set of JSON-RPC constants.

    :param node: Information required to connect to a node.
    :returns: A list of all supported RPC constants.

    """
    schema = get_rpc_schema(node)

    return sorted([i["name"] for i in schema["methods"]])
