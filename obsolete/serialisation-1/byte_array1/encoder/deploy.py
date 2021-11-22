import typing

from pycspr.serialisation.byte_array.encoder.cl_complex import encode_vector_of_t
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_string
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_byte_array
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_u32
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_u8_array
from pycspr.serialisation.byte_array.encoder.cl_type import encode_cl_type
from pycspr.serialisation.byte_array.encoder.cl_value import encode as encode_cl_value
from pycspr.types import Deploy
from pycspr.types import DeployHeader
from pycspr.types import DeployArgument
from pycspr.types import DeployExecutableItem
from pycspr.types import ModuleBytes
from pycspr.types import StoredContractByHash
from pycspr.types import StoredContractByHashVersioned
from pycspr.types import StoredContractByName
from pycspr.types import StoredContractByNameVersioned
from pycspr.types import Transfer


def encode_deploy(entity: Deploy) -> bytes:
    """Encodes a deploy.

    """
    raise NotImplementedError()


def encode_deploy_header(entity: DeployHeader) -> bytes:
    """Encodes a deploy header.

    """
    raise NotImplementedError()


def encode_execution_argument(entity: DeployArgument) -> bytes:
    """Encodes an execution argument.

    """
    print("000", entity.value)
    print("000", encode_cl_value(entity.value))
    # print(111, encode_u8_array(encode_cl_value(entity.value)))
    return \
        encode_string(entity.name) + \
        encode_u8_array(encode_cl_value(entity.value)) + \
        encode_cl_type(entity.value.cl_type)


def encode_execution_arguments(args: typing.List[DeployArgument]) -> bytes:
    """Encodes an execution argument.

    """
    return encode_vector_of_t(list(map(encode_execution_argument, args)))


def encode_executable_deploy_item(entity: DeployExecutableItem) -> bytes:
    """Encodes execution information for subsequent interpretation by VM.

    """
    if isinstance(entity, ModuleBytes):
        return bytes([0]) + \
               encode_u8_array(list(entity.module_bytes)) + \
               encode_execution_arguments(entity.args)

    elif isinstance(entity, StoredContractByHash):
        return bytes([1]) + \
               encode_byte_array(entity.hash) + \
               encode_string(entity.entry_point) + \
               encode_execution_arguments(entity.args)

    elif isinstance(entity, StoredContractByHashVersioned):
        return bytes([2]) + \
               encode_byte_array(entity.hash) + \
               encode_u32(entity.version) + \
               encode_string(entity.entry_point) + \
               encode_execution_arguments(entity.args)

    elif isinstance(entity, StoredContractByName):
        return bytes([3]) + \
               encode_string(entity.name) + \
               encode_string(entity.entry_point) + \
               encode_execution_arguments(entity.args)

    elif isinstance(entity, StoredContractByNameVersioned):
        return bytes([4]) + \
               encode_string(entity.name) + \
               encode_u32(entity.version) + \
               encode_string(entity.entry_point) + \
               encode_execution_arguments(entity.args)

    elif isinstance(entity, Transfer):
        return bytes([5]) + \
               encode_execution_arguments(entity.args)

    else:
        raise ValueError("Unrecognized DeployExecutableItem type")


# Map: Deploy type <-> encoder.
ENCODERS = {
    Deploy: encode_deploy,
    DeployHeader: encode_deploy_header,
    DeployArgument: encode_execution_argument,
    ModuleBytes: encode_executable_deploy_item,
    StoredContractByHash: encode_executable_deploy_item,
    StoredContractByHashVersioned: encode_executable_deploy_item,
    StoredContractByName: encode_executable_deploy_item,
    StoredContractByNameVersioned: encode_executable_deploy_item,
    Transfer: encode_executable_deploy_item,
}


def encode(entity) -> bytes:
    """Encodes a deploy related domain entity as an array of bytes.

    """
    try:
        encoder = ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unencodeable type: {type(entity)}")
    else:
        return encoder(entity)
