import json

import requests

from pycspr.api.node.rest import constants
from pycspr.api.node.rest.connection import ConnectionInfo


class Proxy:
    """Node REST server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.connection_info = connection_info

    @property
    def address(self) -> str:
        """A node's REST server base address."""
        return f"http://{self.connection_info.host}:{self.connection_info.port}"

    def __str__(self):
        """Instance string representation."""
        return self.address

    async def get_chainspec(self) -> dict:
        """Returns network chainspec.

        :returns: Network chainspec.

        """
        return json.loads(
            await self._get_response(constants.ENDPOINT_GET_CHAINSPEC)
        )["chainspec_bytes"]

    async def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        response = await self._get_response(constants.ENDPOINT_GET_METRICS)

        return sorted([i.strip() for i in response.split("\n") if not i.startswith("#")])

    async def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return json.loads(
            await self._get_response(constants.ENDPOINT_GET_STATUS)
        )

    async def get_validator_changes(self) -> list:
        """Returns validator change information.

        :returns: Validator change information.

        """
        return json.loads(
            await self._get_response(constants.ENDPOINT_GET_VALIDATOR_CHANGES)
        )["changes"]

    async def _get_response(self, endpoint: str) -> dict:
        """Invokes remote REST API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :returns: Parsed REST API response.

        """
        return requests.get(f"{self.address}/{endpoint}").content.decode("utf-8")
