from pycspr.api.node.bin.connection import ConnectionInfo


class Proxy:
    """Node BINARY server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self._connection_info = connection_info

    def get_block_header(self) -> bytes:
        pass
