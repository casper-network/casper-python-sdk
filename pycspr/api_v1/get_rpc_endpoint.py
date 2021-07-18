import typing

import jsonrpcclient as rpc_client

import pycspr
from pycspr.api_v1.get_rpc_schema import execute as get_rpc_schema
from pycspr.types import NodeConnectionInfo


def execute(connection_info: NodeConnectionInfo, endpoint: str = None) -> typing.Union[dict, list]:
    """Returns RPC schema.

    :param connection_info: Information required to connect to a node.
    :param endpoint: A specific endpoint of interest.

    :returns: Either list of all RPC endpoints or RPC schema endpoint fragment.

    """
    schema = get_rpc_schema(connection_info)
    if endpoint is None:
        return sorted([i["name"] for i in schema["methods"]])
    else:
        for obj in schema["methods"]:
            if obj["name"].lower() == endpoint.lower():
                return obj
