from pycspr.api.constants import RPC_INFO_GET_STATUS

""" Returns node peers information.

:param node: Information required to connect to a node.
:returns: Node peers information.
"""


def get_rpc_name():
    return RPC_INFO_GET_STATUS


def extract_result(response):
    return response['peers']


def get_params():
    return {}
