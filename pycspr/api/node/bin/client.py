import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin import utils
from pycspr.api.node.bin.proxy import \
    Proxy
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    RequestID
from pycspr.api.node.bin.types.domain import \
    BlockID, \
    BlockHeader, \
    BlockRange, \
    NodeUptime


class Client():
    """Node BINARY server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's BINARY port.

        """
        self.proxy = Proxy(connection_info)

    async def get_information_available_block_range(
        self,
        request_id: RequestID = None
    ) -> BlockRange:
        """Returns a node's available block range.

        :param request_id: Request correlation identifier.
        :returns: A node's available block range.

        """
        pass
        # return codec.decode(
        #     await self.proxy.get_information_available_block_range(request_id)
        # )

    async def get_information_block_header(
        self,
        block_id: typing.Optional[BlockID] = None,
        request_id: RequestID = None
    ) -> BlockHeader:
        """Returns a block header.

        :param block_id: Identifier of a finalised block.
        :param request_id: Request correlation identifier.
        :returns: A block header.

        """
        pass
        # response: bytes = await self.proxy.get_information_block_header(block_id, request_id)

        # print(utils.parse_response(response, request_id))

        # return codec.decode(
        #     await self.proxy.get_information_block_header(block_id, request_id),
        #     BlockHeader
        # )

    async def get_information_uptime(
        self,
        request_id: RequestID = None
    ) -> NodeUptime:
        """Returns node uptime information.

        :param request_id: Request correlation identifier.
        :returns: Node uptime information.

        """
        pass
        # return codec.decode(
        #     await self.proxy.get_information_uptime(request_id)
        # )


    async def get_information_uptime_1(
        self,
        request_id: RequestID = None
    ) -> NodeUptime:
        """Returns node uptime information.

        :param request_id: Request correlation identifier.
        :returns: Node uptime information.

        """
        request = Request(
            Endpoint.Get_Information_Uptime,
            utils.get_request_header(
                self.proxy.connection_info,
                request_id
            )
        )

        return await self.proxy.get_response(request)
