import importlib
import time
from typing import Union

import requests

from pycspr.client.events import NodeConnectionInfo

from pycspr import factory
from pycspr import types


__all__ = ["CasperApi", ]


class CasperApi:

    def __init__(self, node: NodeConnectionInfo):
        self._node = node

    def get_block_at_era_switch(self, polling_interval_seconds: float = 1.0,
                                max_polling_time_seconds: float = 120.0
                                ) -> dict:
        """
        Returns last finalised block in current era.

        :param node: Information required to connect to a node.
        :param polling_interval_seconds: Time interval time (in seconds) before
                                         polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.

        :returns: On-chain block information.
        """
        elapsed = 0.0
        while True:
            block = self.get_block()
            if block["header"]["era_end"] is not None:
                return block
            elapsed += polling_interval_seconds
            if elapsed > max_polling_time_seconds:
                break
            time.sleep(polling_interval_seconds)

    def get_rpc_endpoint(self, endpoint: str) -> Union[dict, list]:
        """
        Returns RPC schema for a single endpoint.

        :param node: Information required to connect to a node.
        :param endpoint: A specific endpoint of interest.
        :returns: JSON-RPC schema endpoint fragment.

        """
        schema = self.get_rpc_schema()
        for obj in schema["methods"]:
            if obj["name"].lower() == endpoint.lower():
                return obj

    def get_rpc_endpoints(self) -> list[str]:
        """
        Returns set of JSON-RPC constants.

        :param node: Information required to connect to a node.
        :returns: A list of all supported RPC constants.
        """
        schema = self.get_rpc_schema()
        return sorted([i["name"] for i in schema["methods"]])

    def get_account_main_purse_uref(self, account_key: Union[bytes, str],
                                    block_id:
                                        Union[None, bytes, str, int] = None
                                    ) -> types.UnforgeableReference:
        """
        Returns an on-chain account's main purse unforgeable reference.

        :param node: Information required to connect to a node.
        :param account_key: Key of an on-chain account.
        :param block_id: Identifier of a finalised block.
        :returns: Account main purse unforgeable reference.
        """
        account_info = self.get_account_info(account_key, block_id)
        return factory.create_uref_from_string(account_info["main_purse"])

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
