from pycspr.api.connection import NodeConnectionInfo
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
        self.proxy = Proxy(connection_info.host, connection_info.port_rpc_speculative)

    def speculative_exec(self, deploy: Deploy, block_id: BlockID = None) -> dict:
        """Dispatches a deploy to a node for speculative execution.

        :param deploy: A deploy to be processed at a node.
        :param block_id: Identifier of a finalised block.
        :returns: Execution effects of virtual deploy processing.

        """
        return self.proxy.speculative_exec(deploy, block_id)
