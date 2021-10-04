import dataclasses
import importlib
import time
from typing import Union

import requests
import jsonrpcclient


from pycspr import factory
from pycspr import types


__all__ = ["CasperApi", "NodeConnectionInfo", "NodeAPIError"]


class NodeAPIError(Exception):
    def __init__(self, msg):
        super(NodeAPIError, self).__init__(msg)


@dataclasses.dataclass
class NodeConnectionInfo:
    """Encapsulates information required to connect to a node.

    """
    # Host address.
    host: str = "localhost"

    # Number of exposed REST port.
    port_rest: int = 8888

    # Number of exposed RPC port.
    port_rpc: int = 7777

    # Number of exposed SSE port.
    port_sse: int = 9999

    @property
    def address(self) -> str:
        """A node's server base address."""
        return f"http://{self.host}"

    @property
    def address_rest(self) -> str:
        """A node's REST server base address."""
        return f"{self.address}:{self.port_rest}"

    @property
    def address_rpc(self) -> str:
        """A node's RPC server base address."""
        return f"{self.address}:{self.port_rpc}/rpc"

    @property
    def address_sse(self) -> str:
        """A node's SSE server base address."""
        return f"{self.address}:{self.port_sse}/events"

    def __str__(self):
        """Instance string representation."""
        return self.host

    def get_response(self, endpoint: str, params: dict = None) -> dict:
        """Invokes remote JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoints parameters.
        :returns: Parsed JSON-RPC response.
        """
        response = requests.post(self.address_rpc,
                                 json=jsonrpcclient.request(endpoint,
                                                            params))
        response = jsonrpcclient.parse(response.json())
        if isinstance(response, jsonrpcclient.responses.Error):
            raise NodeAPIError(response)
        else:
            return response.result


class CasperApi:

    def __init__(self, node: NodeConnectionInfo):
        self._node = node


    def _execute(self, module):
        def _call(*args, **kwargs):
            try:
                # @TODO: error for get_params and extrac_result not existing
                params = module.get_params(*args, **kwargs)
                if 'get_rpc_name' in module.__dict__:
                    response = self._node.get_response(module.get_rpc_name(),
                                                       params)
                elif 'get_rest_name' in module.__dict__:
                    endpoint = (f"{self._node.address_rest}/"
                                f"{module.get_rest_name()}")
                    response = requests.get(endpoint, params)
                else:
                    raise NameError("You have define get_rest_name() or "
                                    "get_rpc_name(), depending on which call "
                                    "(rest or rpc) you want to make.")
                return module.extract_result(response)
            except Exception as e:
                raise e.__class__(f"in {module.__file__}:\n{e}")
        return _call

    def __getattr__(self, attr):
        module = importlib.import_module(f"pycspr.api.{attr}")
        return self._execute(module)
