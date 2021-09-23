class NodeAPIError(Exception):
    """Node API error wrapper.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(NodeAPIError, self).__init__(msg)
