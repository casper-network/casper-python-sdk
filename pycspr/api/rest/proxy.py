import dataclasses
import json

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

    def get_chainspec(self) -> dict:
        """Returns network chainspec.

        :returns: Network chainspec.

        """
        response: str = self.get_response(constants.REST_GET_CHAINSPEC)

        return json.loads(response)["chainspec_bytes"]

    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        response = self.get_response(constants.REST_GET_METRICS)

        return sorted([i.strip() for i in response.split("\n") if not i.startswith("#")])

    def get_rpc_schema(self) -> dict:
        """Returns node RPC API schema.

        :returns: Node RPC API schema.

        """
        response: str = self.get_response(constants.REST_GET_RPC_SCHEMA)

        return json.loads(response)

    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return json.loads(self.get_response(constants.REST_GET_STATUS))

    def get_validator_changes(self) -> list:
        """Returns validator change information.

        :returns: Validator change information.

        """
        response = self.get_response(constants.REST_GET_VALIDATOR_CHANGES)

        return json.loads(response)["changes"]
