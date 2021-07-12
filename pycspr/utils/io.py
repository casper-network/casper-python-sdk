import json
import pathlib
import typing

from pycspr import codec
from pycspr.types.deploy import Deploy



def read_deploy(filepath: typing.Union[pathlib.Path, str]) -> Deploy:
    """Read a deploy from file system.

    :filepath: Path to target file.
    
    """
    filepath = pathlib.Path(filepath) if isinstance(filepath, str) else filepath
    with open(str(filepath), "r") as fstream:
        return codec.from_json(json.loads(fstream.read()))


def write_deploy(deploy: Deploy, filepath: typing.Union[pathlib.Path, str], force: bool = True):
    """Writes a deploy to file system.

    :deploy: Deploy to be written in JSON format.
    :filepath: Path to target file.
    :force: Flag indicating whether deploy will be written if a file already exists.
    
    """
    filepath = pathlib.Path(filepath) if isinstance(filepath, str) else filepath
    if not force and filepath.exists():
        raise IOError("Deploy has already been written to file system")

    with open(str(filepath), "w") as fstream:
        fstream.writelines(codec.to_json(deploy))
