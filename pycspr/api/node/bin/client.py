import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin.proxy import Proxy
from pycspr.api.node.bin.types.chain import \
    AvailableBlockRange, \
    BlockID, \
    BlockHeader, \
    BlockSynchronizerStatus, \
    ChainspecRawBytes, \
    ConsensusStatus, \
    EraID, \
    NextUpgrade
from pycspr.api.node.bin.types.node import \
    NodeLastProgress, \
    NodePeerEntry, \
    NodeUptime
from pycspr.api.node.bin.types.crypto import PublicKey
from pycspr.api.node.bin.types.primitives.numeric import U8
from pycspr.api.node.bin.types.transport import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    Request as ProxyRequest, \
    RequestID, \
    Response, \
    Response as ProxyResponse


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
    ) -> Response:
        """Returns a node's available block range.

        :param request_id: Request correlation identifier.
        :returns: A node's available block range.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_AvailableBlockRange,
        )

    async def get_information_block_header(
        self,
        request_id: RequestID,
        block_id: typing.Optional[BlockID] = None,
    ) -> Response:
        """Returns a block header. Defaults to most recent.

        :param request_id: Request correlation identifier.
        :param block_id: Identifier of a finalised block.
        :returns: A block header.

        """
        def get_request_payload() -> typing.Optional[bytes]:
            return codec.encode(block_id, BlockID, is_optional=True)

        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_BlockHeader,
            get_request_payload()
        )

    async def get_information_chainspec_rawbytes(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns raw bytes representation of chain specification.

        :param request_id: Request correlation identifier.
        :returns: Raw shain specification.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_ChainspecRawBytes,
        )

    async def get_information_consensus_status(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns current consensus status.

        :param request_id: Request correlation identifier.
        :returns: Current consensus status.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_ConsensusStatus,
        )

    async def get_information_latest_switch_block_header(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns latest switch block header.

        :param request_id: Request correlation identifier.
        :returns: A block header.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_LatestSwitchBlockHeader,
        )

    async def get_information_network_name(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns name of network in which a node is participating within.

        :param request_id: Request correlation identifier.
        :returns: Name of network.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_NetworkName,
        )

    async def get_information_network_next_upgrade(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns next point in time at which network is scheduled to be upgraded.

        :param request_id: Request correlation identifier.
        :returns: Next point in time at which network is scheduled to be upgraded.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_NextUpgrade,
        )

    async def get_information_node_block_synchronizer_status(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns a block syncronization status.

        :param request_id: Request correlation identifier.
        :returns: A node's available block range.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_BlockSynchronizerStatus,
        )

    async def get_information_node_last_progress(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns a node's last progress.

        :param request_id: Request correlation identifier.
        :returns: Timestamp corresponding to when the node's linear chain view last progressed.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_LastProgress,
        )

    async def get_information_node_peers(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns node peers information.

        :param request_id: Request correlation identifier.
        :returns: Node peers information.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_Peers,
        )

    async def get_information_node_reactor_state(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns node peers information.

        :param request_id: Request correlation identifier.
        :returns: Node peers information.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_ReactorState,
        )

    async def get_information_node_uptime(
        self,
        request_id: RequestID,
    ) -> Response:
        """Returns node uptime information.

        :param request_id: Request correlation identifier.
        :returns: Node uptime information.

        """
        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_Uptime,
        )

    async def get_information_reward_by_block(
        self,
        request_id: RequestID,
        validator_id: PublicKey,
        delegator_id: typing.Optional[PublicKey] = None,
        block_id: typing.Optional[BlockID] = None,
    ) -> Response:
        """Returns POS reward information.

        :param request_id: Request correlation identifier.
        :param validator_id: Identity of a network validator.
        :param block_id: A block within an era for which POS reward information is being requested.
        :param delegator_id: Identity of a network delegator.
        :returns: POS reward information.

        """
        raise NotImplementedError()


    async def get_information_reward_by_era(
        self,
        request_id: RequestID,
        validator_id: PublicKey,
        delegator_id: typing.Optional[PublicKey] = None,
        era_id: typing.Optional[EraID] = None,
    ) -> Response:
        """Returns POS reward information.

        :param request_id: Request correlation identifier.
        :param validator_id: Identity of a network validator.
        :param era_id: Era for which POS reward information is being requested.
        :param delegator_id: Identity of a network delegator.
        :returns: POS reward information.

        """
        def get_request_payload() -> bytes:
            return \
                codec.encode(1, U8) + \
                codec.encode(0, U8) + \
                codec.encode(era_id, EraID) + \
                codec.encode(validator_id, PublicKey) + \
                codec.encode(delegator_id, PublicKey, is_optional=True)

        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_Reward,
            get_request_payload()
        )

    async def get_information_signed_block(
        self,
        request_id: RequestID,
        block_id: typing.Optional[BlockID] = None,
    ) -> Response:
        """Returns a signed block. Defaults to most recent.

        :param request_id: Request correlation identifier.
        :param block_id: Identifier of a finalised block.
        :returns: A signed block.

        """
        def get_request_payload() -> typing.Optional[bytes]:
            return codec.encode(block_id, BlockID, is_optional=True)

        return await self.proxy.get_response(
            request_id,
            Endpoint.Get_Information_SignedBlock,
            get_request_payload()
        )
