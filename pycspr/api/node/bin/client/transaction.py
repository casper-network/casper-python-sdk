import typing

from pycspr.api.node.bin.proxy import Proxy
from pycspr.type_defs.chain import Transaction
from pycspr.api.node.bin.type_defs import \
    Endpoint, \
    RequestID, \
    Response


class TransactionClient():
    """Encapsulates transaction specific endpoints.

    """
    def __init__(self, proxy: Proxy):
        """Instance constructor.

        :param proxy: Proxy to a node's BINARY port.

        """
        self.proxy = proxy

    async def try_accept(
        self,
        request_id: RequestID,
        transaction: Transaction
    ) -> Response:
        """Dispatches a transaction to the node for inclusion.

        :param request_id: Request correlation identifier.
        :param transaction: A transaction to be dispatched into network for inclusion.
        :returns: Binary API proxy response.

        """
        raise NotImplementedError(123)

    async def try_speculative_execution(
        self,
        request_id: RequestID,
        transaction: Transaction
    ) -> Response:
        """Dispatches a transaction to the node for speculative execution.

        :param request_id: Request correlation identifier.
        :param transaction: A transaction to be dispatched into network for speculative execution.
        :returns: Binary API proxy response.

        """
        raise NotImplementedError()
