#  8b,dPPYba,   8b       d8   ,adPPYba,  ,adPPYba,  8b,dPPYba,   8b,dPPYba,  
#  88P'    "8a  `8b     d8'  a8"     ""  I8[    ""  88P'    "8a  88P'   "Y8  
#  88       d8   `8b   d8'   8b           `"Y8ba,   88       d8  88          
#  88b,   ,a8"    `8b,d8'    "8a,   ,aa  aa    ]8I  88b,   ,a8"  88          
#  88`YbbdP"'       Y88'      `"Ybbd8"'  `"YbbdP"'  88`YbbdP"'   88          
#  88               d8'                             88                       
#  88              d8'                              88                       


from pycspr               import crypto
from pycspr               import factory
from pycspr               import types
from pycspr.api           import get_account_balance
from pycspr.api           import get_account_info
from pycspr.api           import get_account_info_by_account_hash
from pycspr.api           import get_account_main_purse_uref
from pycspr.api           import get_auction_info
from pycspr.api           import get_block
from pycspr.api           import get_block_transfers
from pycspr.api           import get_deploy
from pycspr.api           import get_era_info
from pycspr.api           import get_events
from pycspr.api           import get_node_metrics
from pycspr.api           import get_node_peers
from pycspr.api           import get_node_status
from pycspr.api           import get_rpc_endpoint
from pycspr.api           import get_rpc_schema
from pycspr.api           import get_state_item
from pycspr.api           import get_state_root_hash
from pycspr.api           import get_switch_block
from pycspr.crypto        import get_account_hash as get_account_address
from pycspr.crypto        import get_account_hash
from pycspr.crypto        import get_account_key
from pycspr.types.node    import NodeConnectionInfo
from pycspr.types.node    import NodeEventType
from pycspr.types.node    import NODE_REST_ENDPOINTS
from pycspr.types.node    import NODE_RPC_ENDPOINTS
from pycspr.types.node    import NODE_SSE_ENDPOINTS
from pycspr.serialization import decode
from pycspr.serialization import encode
from pycspr.serialization import CLEncoding
from pycspr.serialization import CLType



# Lib metadata.
__title__ = "pycspr"
__version__ = "0.3.0"
__author__ = "Mark A. Greenslade"
__license__ = "Apache 2.0"

# Node connection info.
CONNECTION = None


def initialise(connection_info: NodeConnectionInfo):
    """Library initialiser - to be invoked prior to usage.
    
    :param connection_info: Information required to connect to a node.
    
    """
    global CONNECTION

    assert isinstance(connection_info, NodeConnectionInfo)

    if CONNECTION is None:
        CONNECTION = connection_info

