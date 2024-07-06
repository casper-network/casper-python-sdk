from pycspr.api.node.bin import codec
from pycspr.api.node.bin import types
from pycspr.api.node.bin import utils
from pycspr.api.node.bin.connection import ConnectionInfo
from pycspr.api.node.bin.types.request.core import RequestType
from pycspr.api.node.bin.types.domain import BlockID


class Proxy:
    """Node BINARY server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self._connection_info = connection_info

    async def get_information_block_header(self, block_id: BlockID = None) -> bytes:
        request = utils.get_request(
            RequestType.Get,
            types.request.get.information.GetBlockHeaderRequest(block_id)
        )

        return await utils.get_response(self._connection_info, request)


    async def get_information_uptime(self) -> bytes:
        request = utils.get_request(
            RequestType.Get,
            types.request.get.information.GetUptimeRequest()
        )

        return await utils.get_response(self._connection_info, request)
