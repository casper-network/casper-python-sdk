import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.connection import ConnectionInfo
from pycspr.api.node.bin.proxy import Proxy
from pycspr.api.node.bin.types.domain import BlockID
from pycspr.api.node.bin.types.domain import BlockHeader
from pycspr.api.node.bin.types.domain import NodeUptimeInfo


class Client():
    """Node BINARY server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's BINARY port.

        """
        self.proxy = Proxy(connection_info)

    async def get_information_block_header(self, block_id: BlockID = None) -> BlockHeader:
        """Returns a block header.

        :param block_id: Identifier of a finalised block.
        :returns: A block header.

        """
        return codec.decode(
            await self.proxy.get_information_block_header(block_id)
        )

    async def get_information_uptime(self) -> NodeUptimeInfo:
        """Returns node uptime information.

        :returns: Node uptime information.

        """
        return codec.decode(
            await self.proxy.get_information_uptime()
        )
