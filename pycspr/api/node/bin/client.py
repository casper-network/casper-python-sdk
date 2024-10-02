import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.proxy import \
    Proxy
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
    RequestID, \
    Response
from pycspr.api.node.bin.types.chain import \
    BlockID, \
    BlockHeader, \
    BlockRange
from pycspr.api.node.bin.types.node import \
    NodePeerEntry, \
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
        request_id: RequestID,
        decode: bool = True,
    ) -> BlockRange:
        """Returns a node's available block range.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: A node's available block range.

        """
        raise NotImplementedError()

    async def get_information_block_header(
        self,
        request_id: RequestID,
        block_id: typing.Optional[BlockID] = None,
        decode: bool = True,
    ) -> BlockHeader:
        """Returns a block header. Defaults to most recent.

        :param request_id: Request correlation identifier.
        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: A block header.

        """
        # Set payload.
        payload = bytes([])
        if block_id is not None:
            payload += codec.encode(block_id, BlockID, is_optional=True)

        # Set response.
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_BlockHeader,
            request_id,
            payload
        )

        # Return
        return _parse_response(response, BlockHeader, decode)

    async def get_information_node_peers(
        self,
        request_id: RequestID,
        decode: bool = True,
    ) -> typing.Union[Response, typing.List[NodePeerEntry]]:
        """Returns node peers information.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Node peers information.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_Peers,
            request_id,
        )

        return _parse_response(response, NodePeerEntry, decode, is_sequence=True)

    async def get_information_node_uptime(
        self,
        request_id: RequestID,
        decode: bool = True
    ) -> typing.Union[Response, NodeUptime]:
        """Returns node uptime information.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Node uptime information.

        """
        response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_Uptime,
            request_id,
        )

        return _parse_response(response, NodeUptime, decode)


def _parse_response(
    response: Response,
    typedef: type,
    decode: bool,
    is_sequence: bool = False
) -> typing.Union[Response, typing.Union[object, typing.List[object]]]:
    """Utility function to parse a response.

    """
    if decode is True:
        bytes_rem, entity = codec.decode(response.bytes_payload, typedef, is_sequence=is_sequence)
        assert len(bytes_rem) == 0, "Byte stream only partially decoded"
        return entity

    return response
