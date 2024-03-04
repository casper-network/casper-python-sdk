from pycspr import serialisation
from pycspr.api import constants
from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rpc.utils import params as param_utils
from pycspr.api.rpc_speculative.proxy import Proxy
from pycspr.types import Deploy
from pycspr.types import BlockID


class Client():
    """Node speculative RPC server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo) -> dict:
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        print(connection_info)
        print("qwewqeeq", connection_info.port_rpc_speculative)
        self.proxy = Proxy(connection_info.host, connection_info.port_rpc_speculative)

    def speculative_exec(self, deploy: Deploy, block_id: BlockID = None) -> dict:
        """Dispatches a deploy to a node for speculative execution.

        :param deploy: A deploy to be processed at a node.
        :param block_id: Identifier of a finalised block.
        :returns: Execution effects of virtual deploy processing.

        """
        params: dict = param_utils.get_block_id(block_id) | {
            "deploy": serialisation.to_json(deploy)
        }
        response: dict = self.proxy.get_response(constants.SPECULATIVE_RPC_EXEC_DEPLOY, params)

        return response["execution_result"]
