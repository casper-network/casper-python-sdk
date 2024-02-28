from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rest import Client as RestClient
from pycspr.api.rpc import Client as RpcClient
from pycspr.api.rpc_speculative import Client as SpeculativeRpcClient
from pycspr.api.sse import Client as SseClient


class NodeClient():
    """Node client that wraps sub-clients to expose a single interface for interacting  with a node.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection: Information required to connect to a node.

        """
        self._rest_client = RestClient(connection_info)
        self._rpc_client = RpcClient(connection_info)
        self._speculative_rpc_client = SpeculativeRpcClient(connection_info)
        self._sse_client = SseClient(connection_info, self._rpc_client)

        # REST server function set.
        self.get_node_metrics = self._rest_client.get_node_metrics
        self.get_node_metric = self._rest_client.ext.get_node_metric

        # RPC server function set.
        self.get_account_balance = self._rpc_client.get_account_balance
        self.get_account_info = self._rpc_client.get_account_info
        self.get_account_main_purse_uref = self._rpc_client.ext.get_account_main_purse_uref
        self.get_account_named_key = self._rpc_client.ext.get_account_main_purse_uref
        self.get_auction_info = self._rpc_client.get_auction_info
        self.get_block = self._rpc_client.get_block
        self.get_block_at_era_switch = self._rpc_client.ext.get_block_at_era_switch
        self.get_block_height = self._rpc_client.ext.get_block_height
        self.get_block_transfers = self._rpc_client.get_block_transfers
        self.get_chain_heights = self._rpc_client.ext.get_chain_heights
        self.get_chain_spec = self._rpc_client.get_chainspec
        self.get_deploy = self._rpc_client.get_deploy
        self.get_dictionary_item = self._rpc_client.get_dictionary_item
        self.get_era_height = self._rpc_client.ext.get_era_height
        self.get_era_info = self._rpc_client.get_era_info_by_switch_block
        self.get_era_info_by_switch_block = self._rpc_client.get_era_info_by_switch_block
        self.get_era_summary = self._rpc_client.get_era_summary
        self.get_node_peers = self._rpc_client.get_node_peers
        self.get_node_status = self._rpc_client.get_node_status
        self.get_rpc_schema = self._rpc_client.get_rpc_schema
        self.get_state_item = self._rpc_client.get_state_item
        self.get_state_key_value = self._rpc_client.get_state_key_value
        self.get_state_root = self.get_state_root_hash = self._rpc_client.get_state_root
        self.get_validator_changes = self._rpc_client.get_validator_changes
        self.get_rpc_endpoint = self._rpc_client.ext.get_rpc_endpoint
        self.get_rpc_endpoints = self._rpc_client.ext.get_rpc_endpoints
        self.send_deploy = self._rpc_client.account_put_deploy

        # RPC server (speculative) function set.
        self.speculative_exec = self._speculative_rpc_client.speculative_exec

        # SSE server function set.
        self.await_n_blocks = self._sse_client.ext.await_n_blocks
        self.await_n_eras = self._sse_client.ext.await_n_eras
        self.await_n_events = self._sse_client.ext.await_n_events
        self.await_until_block_n = self._sse_client.ext.await_until_block_n
        self.await_until_era_n = self._sse_client.ext.await_until_era_n
        self.get_events = self._sse_client.ext.get_events
        self.yield_events = self._sse_client.yield_events
