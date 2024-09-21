from pycspr.api.sidecar.rpc_speculative.connection import ConnectionInfo
from pycspr.api.sidecar.rpc_speculative.proxy import Proxy
from pycspr.types.node import Deploy
from pycspr.types.node import BlockID


class Client():
    """Node speculative RPC server client.

    """
    def __init__(self, connection_info: ConnectionInfo) -> dict:
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.proxy = Proxy(connection_info)

    async def speculative_exec(self, deploy: Deploy, block_id: BlockID = None) -> dict:
        """Dispatches a deploy to a node for speculative execution.

        :param deploy: A deploy to be processed at a node.
        :param block_id: Identifier of a finalised block.
        :returns: Execution effects of virtual deploy processing.

        """
        return await self.proxy.speculative_exec(deploy, block_id)
