import pathlib
import typing

import requests
import jsonrpcclient

from pycspr import serialisation
from pycspr.types.deploy import Deploy
from pycspr.utils.exceptions import NodeAPIError



def read_deploy(fpath: typing.Union[pathlib.Path, str]) -> Deploy:
    """Reads a deploy from file system.

    :fpath: Path to target file.
    
    """
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    with open(str(fpath), "r") as fstream:
        return serialisation.from_json(fstream.read())


def read_wasm(fpath: typing.Union[pathlib.Path, str]) -> bytes:
    """Read a smart contract from file system.

    :fpath: Path to target file.
    
    """
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    with open(fpath, 'rb') as fstream:
        return fstream.read()


def write_deploy(deploy: Deploy, fpath: typing.Union[pathlib.Path, str], force: bool = True) -> str:
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
        fstream.writelines(serialisation.to_json(deploy))

    return str(fpath)


def get_api_response(node, endpoint: str, params: dict) -> dict:
    """Invokes remote JSON-RPC API and returns parsed response.

    :node: Node connection wrapper.
    :endpoint: Target endpoint to invoke.
    :params: Endpoints parameters.
    :returns: Parsed JSON-RPC response.
    
    """
    response = requests.post(
        node.address_rpc,
        json=jsonrpcclient.request(endpoint, params),
        )
    response = jsonrpcclient.parse(response.json())

    if isinstance(response, jsonrpcclient.responses.Error):
        raise NodeAPIError(response)
    else:
        return response.result
