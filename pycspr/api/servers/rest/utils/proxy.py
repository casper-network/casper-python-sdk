import dataclasses

import requests

from pycspr.api import constants


@dataclasses.dataclass
class Proxy:
    """Node REST server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed REST port.
    port: int = constants.DEFAULT_PORT_REST

    @property
    def address(self) -> str:
        """A node's REST server base address."""
        return f"http://{self.host}:{self.port}"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def get_response(self, endpoint: str) -> dict:
        """Invokes remote REST API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :returns: Parsed REST API response.

        """
        return requests.get(f"{self.address}/{endpoint}").content.decode("utf-8")
