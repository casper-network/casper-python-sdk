import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.proxy import \
    Proxy
from pycspr.api.node.bin.types.transport import \
    ConnectionInfo, \
    Endpoint, \
    RequestID, \
    Response
from pycspr.api.node.bin.types.chain import \
    AvailableBlockRange, \
    BlockID, \
    BlockHeader, \
    ChainspecRawBytes, \
    ConsensusStatus
from pycspr.api.node.bin.types.node import \
    NodeLastProgress, \
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
    ) -> typing.Union[Response, AvailableBlockRange]:
        """Returns a node's available block range.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: A node's available block range.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_AvailableBlockRange,
            request_id,
        )

        return _parse_response(response, AvailableBlockRange, decode)

    async def get_information_block_header(
        self,
        request_id: RequestID,
        block_id: typing.Optional[BlockID] = None,
        decode: bool = True,
    ) -> typing.Union[Response, BlockHeader]:
        """Returns a block header. Defaults to most recent.

        :param request_id: Request correlation identifier.
        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: A block header.

        """
        def get_payload() -> typing.Optional[bytes]:
            if block_id is not None:
                return codec.encode(block_id, BlockID, is_optional=True)

        async def get_response() -> Response:
            return await self.proxy.invoke_endpoint(
                Endpoint.Get_Information_BlockHeader,
                request_id,
                get_payload()
            )

        return _parse_response(await get_response(), BlockHeader, decode)

    async def get_information_chainspec_rawbytes(
        self,
        request_id: RequestID,
        decode: bool = True,
    ) -> typing.Union[Response, ChainspecRawBytes]:
        """Returns raw bytes representation of chain specification.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Raw shain specification.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_ChainspecRawBytes,
            request_id,
        )

        return _parse_response(response, ChainspecRawBytes, decode)

    async def get_information_consensus_status(
        self,
        request_id: RequestID,
        decode: bool = True,
    ) -> typing.Union[Response, ConsensusStatus]:
        """Returns current consensus status.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Current consensus status.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_ConsensusStatus,
            request_id,
        )

        return _parse_response(response, ConsensusStatus, decode)

    async def get_information_network_name(
        self,
        request_id: RequestID,
        decode: bool = True,
    ) -> typing.Union[Response, str]:
        """Returns name of network in which a node is participating within.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Name of network.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_NetworkName,
            request_id,
        )

        return _parse_response(response, str, decode)

    async def get_information_node_last_progress(
        self,
        request_id: RequestID,
        decode: bool = True,
    ) -> typing.Union[Response, NodeLastProgress]:
        """Returns a node's last progress.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Timestamp corresponding to when the node's linear chain view last progressed.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_LastProgress,
            request_id,
        )

        return _parse_response(response, NodeLastProgress, decode)

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

    async def get_information_node_reactor_state(
        self,
        request_id: RequestID,
        decode: bool = True,
    ) -> typing.Union[Response, str]:
        """Returns node peers information.

        :param request_id: Request correlation identifier.
        :param decode: Flag indicating whether to decode response bytes to a domain type instance.
        :returns: Node peers information.

        """
        response: Response = await self.proxy.invoke_endpoint(
            Endpoint.Get_Information_ReactorState,
            request_id,
        )

        return _parse_response(response, str, decode, is_sequence=False)

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
    if decode is False:
        return response

    bytes_rem, entity = codec.decode(typedef, response.bytes_payload, is_sequence=is_sequence)
    assert len(bytes_rem) == 0, "Byte stream only partially decoded"

    return entity
