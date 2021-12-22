from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_types import CL_TypeKey
from pycspr.types.cl_types import CL_Type_Any
from pycspr.types.cl_types import CL_Type_Bool
from pycspr.types.cl_types import CL_Type_ByteArray
from pycspr.types.cl_types import CL_Type_I32
from pycspr.types.cl_types import CL_Type_I64
from pycspr.types.cl_types import CL_Type_U8
from pycspr.types.cl_types import CL_Type_U32
from pycspr.types.cl_types import CL_Type_U64
from pycspr.types.cl_types import CL_Type_U128
from pycspr.types.cl_types import CL_Type_U256
from pycspr.types.cl_types import CL_Type_U512
from pycspr.types.cl_types import CL_Type_Key
from pycspr.types.cl_types import CL_Type_List
from pycspr.types.cl_types import CL_Type_Map
from pycspr.types.cl_types import CL_Type_Option
from pycspr.types.cl_types import CL_Type_PublicKey
from pycspr.types.cl_types import CL_Type_Result
from pycspr.types.cl_types import CL_Type_String
from pycspr.types.cl_types import CL_Type_Tuple1
from pycspr.types.cl_types import CL_Type_Tuple2
from pycspr.types.cl_types import CL_Type_Tuple3
from pycspr.types.cl_types import CL_Type_Unit
from pycspr.types.cl_types import CL_Type_URef

from pycspr.types.cl_values import CL_Value
from pycspr.types.cl_values import CL_Any
from pycspr.types.cl_values import CL_Bool
from pycspr.types.cl_values import CL_ByteArray
from pycspr.types.cl_values import CL_I32
from pycspr.types.cl_values import CL_I64
from pycspr.types.cl_values import CL_U8
from pycspr.types.cl_values import CL_U32
from pycspr.types.cl_values import CL_U64
from pycspr.types.cl_values import CL_U128
from pycspr.types.cl_values import CL_U256
from pycspr.types.cl_values import CL_U512
from pycspr.types.cl_values import CL_Key
from pycspr.types.cl_values import CL_KeyType
from pycspr.types.cl_values import CL_List
from pycspr.types.cl_values import CL_Map
from pycspr.types.cl_values import CL_Option
from pycspr.types.cl_values import CL_PublicKey
from pycspr.types.cl_values import CL_Result
from pycspr.types.cl_values import CL_String
from pycspr.types.cl_values import CL_Tuple1
from pycspr.types.cl_values import CL_Tuple2
from pycspr.types.cl_values import CL_Tuple3
from pycspr.types.cl_values import CL_Unit
from pycspr.types.cl_values import CL_URefAccessRights
from pycspr.types.cl_values import CL_URef

from pycspr.types.deploys import Deploy
from pycspr.types.deploys import DeployApproval
from pycspr.types.deploys import DeployArgument
from pycspr.types.deploys import DeployBody
from pycspr.types.deploys import DeployHeader
from pycspr.types.deploys import DeployParameters
from pycspr.types.deploys import DeployTimeToLive
from pycspr.types.deploys import DeployExecutableItem
from pycspr.types.deploys import ModuleBytes
from pycspr.types.deploys import StoredContract
from pycspr.types.deploys import StoredContractByHash
from pycspr.types.deploys import StoredContractByHashVersioned
from pycspr.types.deploys import StoredContractByName
from pycspr.types.deploys import StoredContractByNameVersioned
from pycspr.types.deploys import Transfer

from pycspr.types.identifiers import AccountID
from pycspr.types.identifiers import BlockID
from pycspr.types.identifiers import ContractID
from pycspr.types.identifiers import ContractVersion
from pycspr.types.identifiers import DeployID
from pycspr.types.identifiers import DictionaryID
from pycspr.types.identifiers import DictionaryID_AccountNamedKey
from pycspr.types.identifiers import DictionaryID_ContractNamedKey
from pycspr.types.identifiers import DictionaryID_SeedURef
from pycspr.types.identifiers import DictionaryID_UniqueKey
from pycspr.types.identifiers import GlobalStateID
from pycspr.types.identifiers import GlobalStateIDType
from pycspr.types.identifiers import StateRootHash

from pycspr.types.keys import PrivateKey
from pycspr.types.keys import PublicKey

from pycspr.types.timestamp import Timestamp


CL_TYPEKEY_TO_CL_VALUE_TYPE = {
    CL_TypeKey.ANY: CL_Any,
    CL_TypeKey.BOOL: CL_Bool,
    CL_TypeKey.BYTE_ARRAY: CL_ByteArray,
    CL_TypeKey.I32: CL_I32,
    CL_TypeKey.I64: CL_I64,
    CL_TypeKey.KEY: CL_Key,
    CL_TypeKey.LIST: CL_List,
    CL_TypeKey.MAP: CL_Map,
    CL_TypeKey.OPTION: CL_Option,
    CL_TypeKey.PUBLIC_KEY: CL_PublicKey,
    CL_TypeKey.RESULT: CL_Result,
    CL_TypeKey.STRING: CL_String,
    CL_TypeKey.TUPLE_1: CL_Tuple1,
    CL_TypeKey.TUPLE_2: CL_Tuple2,
    CL_TypeKey.TUPLE_3: CL_Tuple3,
    CL_TypeKey.U8: CL_U8,
    CL_TypeKey.U32: CL_U32,
    CL_TypeKey.U64: CL_U64,
    CL_TypeKey.U128: CL_U128,
    CL_TypeKey.U256: CL_U256,
    CL_TypeKey.U512: CL_U512,
    CL_TypeKey.UNIT: CL_Unit,
    CL_TypeKey.UREF: CL_URef,
}

CL_TYPEKEY_TO_CL_TYPE = {
    CL_TypeKey.ANY: CL_Type_Any,
    CL_TypeKey.BOOL: CL_Type_Bool,
    CL_TypeKey.BYTE_ARRAY: CL_Type_ByteArray,
    CL_TypeKey.I32: CL_Type_I32,
    CL_TypeKey.I64: CL_Type_I64,
    CL_TypeKey.KEY: CL_Type_Key,
    CL_TypeKey.LIST: CL_Type_List,
    CL_TypeKey.MAP: CL_Type_Map,
    CL_TypeKey.OPTION: CL_Type_Option,
    CL_TypeKey.PUBLIC_KEY: CL_Type_PublicKey,
    CL_TypeKey.RESULT: CL_Type_Result,
    CL_TypeKey.STRING: CL_Type_String,
    CL_TypeKey.TUPLE_1: CL_Type_Tuple1,
    CL_TypeKey.TUPLE_2: CL_Type_Tuple2,
    CL_TypeKey.TUPLE_3: CL_Type_Tuple3,
    CL_TypeKey.U8: CL_Type_U8,
    CL_TypeKey.U32: CL_Type_U32,
    CL_TypeKey.U64: CL_Type_U64,
    CL_TypeKey.U128: CL_Type_U128,
    CL_TypeKey.U256: CL_Type_U256,
    CL_TypeKey.U512: CL_Type_U512,
    CL_TypeKey.UNIT: CL_Type_Unit,
    CL_TypeKey.UREF: CL_Type_URef,
}
