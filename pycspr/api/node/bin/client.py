import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin import utils
from pycspr.api.node.bin.proxy import \
    Proxy
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    RequestID, \
    Response
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

    async def get_information_uptime(
        self,
        request_id: RequestID = None,
        decode: bool = True
    ) -> typing.Union[bytes, Response]:
        """Returns node uptime information.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode API response.
        :returns: Node uptime information.

        """
        response: Response = await self.proxy.get_response(
            Endpoint.Get_Information_Uptime,
            request_id,
        )

        return response


    async def _get_response(self, request: Request, decode: bool) -> typing.Union[bytes, Response]:
        """Encodes & hands request to proxy, awaits & optionally decodes response.

        """
        # codec.encode(request, True)
        response: Response = await self.proxy.get_response(request)
        # if decode is False:
        #     return response_bytes

        # bstream, response = codec.decode(response_bytes, Response)
        # assert \
        #     len(bstream) == 0, \
        #     "Response decoding error: unconsumed bytes"
        return response
