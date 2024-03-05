import dataclasses

from pycspr import serialisation
from pycspr.api import constants
from pycspr.api.rpc import params as param_utils
from pycspr.api.rpc.proxy import get_response
from pycspr.types import Deploy
from pycspr.types import BlockID


@dataclasses.dataclass
class Proxy:
    """Node JSON-RPC server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed speculative RPC port.
    port: int = constants.DEFAULT_PORT_SPECULATIVE_RPC

    @property
    def address(self) -> str:
        """A node's RPC server base address."""
        return f"http://{self.host}:{self.port}/rpc"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def speculative_exec(self, deploy: Deploy, block_id: BlockID = None) -> dict:
        """Dispatches a deploy to a node for speculative execution.

        :param deploy: A deploy to be processed at a node.
        :param block_id: Identifier of a finalised block.
        :returns: Execution effects of virtual deploy processing.

        """
        params: dict = param_utils.get_block_id(block_id) | {
            "deploy": serialisation.to_json(deploy)
        }

        return get_response(
            self.address,
            constants.SPECULATIVE_RPC_EXEC_DEPLOY,
            params,
            "execution_result"
            )
