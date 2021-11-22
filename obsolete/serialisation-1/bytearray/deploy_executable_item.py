from pycspr.serialisation.bytearray import cl_byte_array
from pycspr.serialisation.bytearray import cl_string
from pycspr.serialisation.bytearray import cl_u8_array
from pycspr.serialisation.bytearray import cl_u32
from pycspr.serialisation.bytearray import cl_vector
from pycspr.serialisation.bytearray import deploy_argument
from pycspr.types import DeployExecutableItem
from pycspr.types import ModuleBytes
from pycspr.types import StoredContractByHash
from pycspr.types import StoredContractByHashVersioned
from pycspr.types import StoredContractByName
from pycspr.types import StoredContractByNameVersioned
from pycspr.types import Transfer


def from_bytes(value: bytes) -> DeployExecutableItem:
    raise NotImplementedError()


def from_json(obj: dict) -> DeployExecutableItem:
    def _module_bytes(obj):
        return ModuleBytes(
            args=[deploy_argument.from_json(i) for i in obj["args"]],
            module_bytes=bytes.fromhex(obj["module_bytes"])
            )

    def _stored_contract_by_hash(obj) -> dict:
        return StoredContractByHash(
            args=[deploy_argument.from_json(i) for i in obj["args"]],
        )

    def _stored_contract_by_hash_versioned(obj) -> dict:
        return StoredContractByHash(
            args=[deploy_argument.from_json(i) for i in obj["args"]],
        )

    def _stored_contract_by_name(obj) -> dict:
        return StoredContractByName(
            args=[deploy_argument.from_json(i) for i in obj["args"]],
        )

    def _stored_contract_by_name_versioned(obj) -> dict:
        return StoredContractByNameVersioned(
            args=[deploy_argument.from_json(i) for i in object["args"]],
        )

    def _transfer(obj):
        return Transfer(
            args=[deploy_argument.from_json(i) for i in obj["Transfer"]["args"]],
            )

    if "ModuleBytes" in obj:
        return _module_bytes(obj["ModuleBytes"])
    elif "StoredContractByHash" in obj:
        return _stored_contract_by_hash(obj["StoredContractByHash"])
    elif "StoredVersionedContractByHash" in obj:
        return _stored_contract_by_hash_versioned(obj["StoredVersionedContractByHash"])
    elif "StoredContractByName" in obj:
        return _stored_contract_by_name(obj["StoredContractByName"])
    elif "StoredVersionedContractByName" in obj:
        return _stored_contract_by_name_versioned(obj["StoredVersionedContractByName"])
    elif "Transfer" in obj:
        return _transfer(obj["Transfer"])
    else:
        raise NotImplementedError("Unsupported execution information variant")



def to_bytes(entity: DeployExecutableItem) -> bytes:
    def _deploy_args():
        return cl_vector.to_bytes(
            list(map(deploy_argument.to_bytes, entity.args))
            )

    def _module_bytes():
        return bytes([0]) + \
               cl_u8_array.to_bytes(list(entity.module_bytes))

    def _stored_contract_by_hash():
        return bytes([1]) + \
               cl_byte_array.to_bytes(entity.hash) + \
               cl_string.to_bytes(entity.entry_point)

    def _stored_contract_by_hash_versioned():
        return bytes([2]) + \
               cl_byte_array.to_bytes(entity.hash) + \
               cl_u32.to_bytes(entity.version) + \
               cl_string.to_bytes(entity.entry_point)

    def _stored_contract_by_name():
        return bytes([3]) + \
               cl_string.to_bytes(entity.name) + \
               cl_string.to_bytes(entity.entry_point)

    def _stored_contract_by_name_versioned():
        return bytes([4]) + \
               cl_string.to_bytes(entity.name) + \
               cl_u32.to_bytes(entity.version) + \
               cl_string.to_bytes(entity.entry_point)

    def _transfer():
        return bytes([5])

    _ENCODERS = {
        ModuleBytes: _module_bytes,
        StoredContractByHash: _stored_contract_by_hash,
        StoredContractByHashVersioned: _stored_contract_by_hash_versioned,
        StoredContractByName: _stored_contract_by_name,
        StoredContractByNameVersioned: _stored_contract_by_name_versioned,
        Transfer: _transfer,
    }

    return _ENCODERS[type(entity)]() + _deploy_args()


def to_json(entity: DeployExecutableItem) -> dict:
    def _module_bytes() -> dict:
        return {
            "ModuleBytes": {
                "args": [deploy_argument.to_json(i) for i in entity.args],
                "module_bytes": entity.module_bytes.hex()
            }
        }

    def _stored_contract_by_hash() -> dict:
        return {
            "StoredContractByHash": {
                "args": [deploy_argument.to_json(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": entity.hash.hex()
            }
        }

    def _stored_contract_by_hash_versioned() -> dict:
        return {
            "StoredContractByHashVersioned": {
                "args": [deploy_argument.to_json(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": entity.hash.hex(),
                "version": entity.version
            }
        }

    def _stored_contract_by_name() -> dict:
        return {
            "StoredContractByName": {
                "args": [deploy_argument.to_json(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": entity.name
            }
        }

    def _stored_contract_by_name_versioned() -> dict:
        return {
            "StoredContractByNameVersioned": {
                "args": [deploy_argument.to_json(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": entity.name,
                "version": entity.version
            }
        }

    def _transfer() -> dict:
        return {
            "Transfer": {
                "args": [deploy_argument.to_json(i) for i in entity.args]
            }
        }

    _ENCODERS = {
        ModuleBytes: _module_bytes,
        StoredContractByHash: _stored_contract_by_hash,
        StoredContractByHashVersioned: _stored_contract_by_hash_versioned,
        StoredContractByName: _stored_contract_by_name,
        StoredContractByNameVersioned: _stored_contract_by_name_versioned,
        Transfer: _transfer,
    }

    return _ENCODERS[type(entity)]()
