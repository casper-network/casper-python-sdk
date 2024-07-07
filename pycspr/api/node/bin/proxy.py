import typing

from pycspr.api.node.bin import codec
from pycspr.api.node.bin import types
from pycspr.api.node.bin import utils
from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Request, \
    RequestType
from pycspr.api.node.bin.types.domain import BlockID


class Proxy:
    """Node BINARY server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self._connection_info = connection_info

    async def get_information_available_block_range(
        self,
        request_id: int = None
    ) -> bytes:
        return await utils.get_response(
            self._connection_info,
            RequestType.Get,
            types.request.get.information.GetAvailableBlockRangeRequest(),
            request_id
        )

    async def get_information_block_header(
        self,
        block_id: typing.Optional[BlockID] = None,
        request_id: int = None
    ) -> bytes:
        return await utils.get_response(
            self._connection_info,
            RequestType.Get,
            types.request.get.information.GetBlockHeaderRequest(block_id),
            request_id
        )

    async def get_information_uptime(
        self,
        request_id: int = None
    ) -> bytes:
        return await utils.get_response(
            self._connection_info,
            RequestType.Get,
            types.request.get.information.GetUptimeRequest(),
            request_id
        )
