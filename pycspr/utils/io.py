import json
import pathlib
import typing

from pycspr import codec
from pycspr.types.deploy import Deploy



def read_deploy(fpath: typing.Union[pathlib.Path, str]) -> Deploy:
    """Read a deploy from file system.

    :fpath: Path to target file.
    
    """
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    with open(str(fpath), "r") as fstream:
        return codec.from_json(json.loads(fstream.read()))


def write_deploy(deploy: Deploy, fpath: typing.Union[pathlib.Path, str], force: bool = True):
    """Writes a deploy to file system.

    :deploy: Deploy to be written in JSON format.
    :fpath: Path to target file.
    :force: Flag indicating whether deploy will be written if a file already exists.
    
    """
    fpath = pathlib.Path(fpath) if isinstance(fpath, str) else fpath
    if not force and fpath.exists():
        raise IOError("Deploy has already been written to file system")

    with open(str(fpath), "w") as fstream:
        fstream.writelines(codec.to_json(deploy))
