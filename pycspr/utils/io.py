import json
import pathlib
import typing

from pycspr import serialisation
from pycspr import factory
from pycspr.types import Deploy


def get_deploy_size_bytes(deploy: Deploy) -> int:
    """Returns size of a deploy in bytes.

    :deploy: Deploy to be written in JSON format.
    :returns: Size of deploy in bytes.

    """
    size: int = len(deploy.hash)
    for approval in deploy.approvals:
        size += len(approval.signature)
        size += len(approval.signer)
    size += len(serialisation.deploy_to_bytes(deploy.header))
    size += len(serialisation.deploy_to_bytes(
        factory.create_deploy_body(deploy.payment, deploy.session))
        )
    
    return size


def read_deploy(fpath: typing.Union[pathlib.Path, str]) -> Deploy:
    """Reads a deploy from file system.

    :fpath: Path to target file.

    """
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    with open(str(fpath), "r") as fstream:
        return serialisation.deploy_from_json(Deploy, json.loads(fstream.read()))


def read_wasm(fpath: typing.Union[pathlib.Path, str]) -> bytes:
    """Read a smart contract from file system.

    :fpath: Path to target file.

    """
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    with open(fpath, "rb") as fstream:
        return fstream.read()


def write_deploy(
    deploy: Deploy,
    fpath: typing.Union[pathlib.Path, str],
    force: bool = True
) -> str:
    """Writes a deploy to file system.

    :deploy: Deploy to be written in JSON format.
    :fpath: Path to target file.
    :force: Flag indicating whether deploy will be written if a file already exists.
    :returns: Path to written file.

    """
    if not isinstance(fpath, (pathlib.Path, str)):
        raise ValueError("Unrecognized file path type")

    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    if not force and fpath.exists():
        raise IOError("Deploy has already been written to file system")

    with open(str(fpath), "w") as fstream:
        fstream.writelines(json.dumps(serialisation.deploy_to_json(deploy), indent=4))

    return str(fpath)
