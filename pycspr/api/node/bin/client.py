import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.connection import ConnectionInfo
from pycspr.api.node.bin.types.domain import BlockID
from pycspr.api.node.bin.types.domain import BlockHeader
from pycspr.api.node.bin.types.domain import NodeUptimeInfo
from pycspr.api.node.bin.proxy import Proxy


class Client():
    """Node BINARY server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's BINARY port.

        """
        self.proxy = Proxy(connection_info)

    async def get_information_block_header(
        self,
        block_id: BlockID = None,
        decode=True
    ) -> typing.Union[bytes, BlockHeader]:
        """Returns a block header.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: A block header.

        """
        encoded: bytes = await self.proxy.get_information_block_header(block_id)

        return codec.decode(encoded) if decode is True else encoded


    async def get_information_uptime(
        self,
        decode=True
    ) -> typing.Union[bytes, NodeUptimeInfo]:
        """Returns node uptime information.

        :param decode: Flag indicating whether to decode API response.
        :returns: Node uptime information.

        """
        encoded: bytes = await self.proxy.get_information_uptime()

        return codec.decode(encoded) if decode is True else encoded
