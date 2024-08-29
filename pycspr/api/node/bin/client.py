import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.proxy import \
    Proxy
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
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
        request_id: RequestID
    ) -> BlockRange:
        """Returns a node's available block range.

        :param request_id: Request correlation identifier.
        :returns: A node's available block range.

        """
        pass

    async def get_information_block_header(
        self,
        request_id: RequestID,
        block_id: typing.Optional[BlockID] = None,
    ) -> BlockHeader:
        """Returns a block header.

        :param block_id: Identifier of a finalised block.
        :param request_id: Request correlation identifier.
        :returns: A block header.

        """
        pass

    async def get_information_chainspec_raw_bytes(
        self,
        request_id: RequestID,
        decode: bool = True
    ) -> typing.Union[Response, NodeUptime]:
        """Returns chainspec as raw bytes.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode API response.
        :returns: Node uptime information.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_ChainspecRawBytes,
            request_id,
        )

        print(444, response.bytes_payload)

        return response if decode is False else response.bytes_payload


    async def get_information_uptime(
        self,
        request_id: RequestID,
        decode: bool = True
    ) -> typing.Union[Response, NodeUptime]:
        """Returns node uptime information.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode API response.
        :returns: Node uptime information.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_Uptime,
            request_id,
        )

        print(444, response.bytes_payload, codec.decode(response.bytes_payload, NodeUptime))

        return response if decode is False else codec.decode(response.bytes_payload, NodeUptime)
