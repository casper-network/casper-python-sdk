import dataclasses
import enum
import typing

from pycspr.crypto import get_account_hash
from pycspr.crypto import get_account_key
from pycspr.type_defs.cl_types import *
from pycspr.type_defs.cl_values import *
from pycspr.type_defs.crypto import KeyAlgorithm
from pycspr.type_defs.crypto import PublicKey


TYPESET_CLT: set = {
    CLT_Type,
    CLT_TypeKey,
    CLT_Any,
    CLT_Bool,
    CLT_ByteArray,
    CLT_I32,
    CLT_I64,
    CLT_U8,
    CLT_U32,
    CLT_U64,
    CLT_U128,
    CLT_U256,
    CLT_U512,
    CLT_Key,
    CLT_List,
    CLT_Map,
    CLT_Option,
    CLT_PublicKey,
    CLT_Result,
    CLT_String,
    CLT_Tuple1,
    CLT_Tuple2,
    CLT_Tuple3,
    CLT_Unit,
    CLT_URef,
}


TYPESET_CLV: set = {
    CLV_Value,
    CLV_Any,
    CLV_Bool,
    CLV_ByteArray,
    CLV_I32,
    CLV_I64,
    CLV_U8,
    CLV_U32,
    CLV_U64,
    CLV_U128,
    CLV_U256,
    CLV_U512,
    CLV_Key,
    CLV_KeyType,
    CLV_List,
    CLV_Map,
    CLV_Option,
    CLV_PublicKey,
    CLV_Result,
    CLV_String,
    CLV_Tuple1,
    CLV_Tuple2,
    CLV_Tuple3,
    CLV_Unit,
    CLV_URefAccessRights,
    CLV_URef,
}

TYPESET: set = TYPESET_CLT | TYPESET_CLV
