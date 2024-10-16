from pycspr.api.node.bin.client.information import InformationClient
from pycspr.api.node.bin.client.transaction import TransactionClient
from pycspr.api.node.bin.proxy import Proxy
from pycspr.api.node.bin.type_defs import ConnectionInfo


class Client():
    """Node BINARY server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's BINARY port.

        """
        proxy = Proxy(connection_info)
        self.information = InformationClient(proxy)
        self.tx = TransactionClient(proxy)
