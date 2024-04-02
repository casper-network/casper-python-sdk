from pycspr import serializer
from pycspr.api import constants
from pycspr.api.rpc import params as param_utils
from pycspr.api.rpc.proxy import get_response
from pycspr.api.rpc_speculative.connection import ConnectionInfo
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import BlockID


class Proxy:
    """Node speculative JSON-RPC server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.connection_info = connection_info

    @property
    def address(self) -> str:
        """A node's speculative RPC server base address."""
        return f"http://{self.connection_info.host}:{self.connection_info.port}/rpc"

    def __str__(self):
        """Instance string representation."""
        return self.address

    async def speculative_exec(self, deploy: Deploy, block_id: BlockID = None) -> dict:
        """Dispatches a deploy to a node for speculative execution.

        :param deploy: A deploy to be processed at a node.
        :param block_id: Identifier of a finalised block.
        :returns: Execution effects of virtual deploy processing.

        """
        params: dict = param_utils.block_id(block_id) | {
            "deploy": serializer.to_json(deploy)
        }

        return await get_response(
            self.address,
            constants.SPECULATIVE_RPC_EXEC_DEPLOY,
            params,
            "execution_result"
            )
