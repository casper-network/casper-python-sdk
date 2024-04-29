import json
import pathlib
import typing

from pycspr import serializer
from pycspr import factory
from pycspr.types.node import Block
from pycspr.types.node import Deploy

# Domain types that can be written to file system. 
_ENTITY_TYPEDEFS = typing.Union[Block, Deploy]


def get_deploy_size_bytes(deploy: Deploy) -> int:
    """Returns size of a deploy in bytes.

    :deploy: Deploy to be written in JSON format.
    :returns: Size of deploy in bytes.

    """
    size: int = len(deploy.hash)
    for approval in deploy.approvals:
        size += len(approval.signature)
        size += len(approval.signer)
        size += len(serializer.to_bytes(deploy.header))
        size += len(serializer.to_bytes(
            factory.create_deploy_body(deploy.payment, deploy.session))
        )

    return size


def read_block(fpath: typing.Union[pathlib.Path, str]) -> Block:
    """Reads a block from file system.

    :fpath: Path to target file.

    """
    return _read_entity(Block, fpath)


def read_deploy(fpath: typing.Union[pathlib.Path, str]) -> Deploy:
    """Reads a deploy from file system.

    :fpath: Path to target file.

    """
    return _read_entity(Deploy, fpath)


def read_wasm(fpath: typing.Union[pathlib.Path, str]) -> bytes:
    """Read a smart contract from file system.

    :fpath: Path to target file.

    """
    return _read_file(fpath)


def write_block(
    block: Block,
    fpath: typing.Union[pathlib.Path, str],
    force: bool = True
) -> pathlib.Path:
    """Writes a block to file system.

    :deploy: Block to be written in JSON format.
    :fpath: Path to target file.
    :force: Flag indicating whether block will be written if a file already exists.
    :returns: Path to written file.

    """
    return _write_entity(block, fpath, force)


def write_deploy(
    deploy: Deploy,
    fpath: typing.Union[pathlib.Path, str],
    force: bool = True
) -> pathlib.Path:
    """Writes a deploy to file system.

    :deploy: Deploy to be written in JSON format.
    :fpath: Path to target file.
    :force: Flag indicating whether deploy will be written if a file already exists.
    :returns: Path to written file.

    """
    return _write_entity(deploy, fpath, force)


def _read_entity(
    typedef: _ENTITY_TYPEDEFS,
    fpath: typing.Union[pathlib.Path, str]
):
    return serializer.from_json(typedef, json.loads(_read_file(fpath)))


def _read_file(fpath: typing.Union[pathlib.Path, str]) -> bytes:
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    with open(fpath, "rb") as fstream:
        return fstream.read()


def _write_entity(
    entity: _ENTITY_TYPEDEFS,
    fpath: typing.Union[pathlib.Path, str],
    force: bool = True
) -> pathlib.Path:
    if not isinstance(fpath, (pathlib.Path, str)):
        raise ValueError("Unrecognized file path type")

    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    if not force and fpath.exists():
        raise IOError("Entity has already been written to file system")

    with open(str(fpath), "w") as fstream:
        fstream.writelines(json.dumps(serializer.to_json(entity), indent=4))

    return fpath
