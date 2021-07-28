import pathlib
import typing

from pycspr import api
from pycspr.client import NodeConnectionInfo
from pycspr.types import Deploy
from pycspr.utils import io as _io



class DeploysClient():
    """Exposes a set of functions for processing deploys.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info


    def send(self, deploy: Deploy):
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.

        """
        return api.put_deploy(self.connection_info, deploy)


    def read(self, fpath: typing.Union[pathlib.Path, str]) -> Deploy:
        """Returns a deploy deserialized from file system.

        :fpath: Path to target file.
        :returns: A deploy for dispatch.
        
        """
        return _io.read_deploy(fpath)


    def write(self, deploy: Deploy, fpath: typing.Union[pathlib.Path, str], force: bool = True):
        """Writes a deploy to file system.

        :param deploy: Deploy to be written in JSON format.
        :param fpath: Path to target file.
        :param force: Flag indicating whether deploy will be written if a file already exists.
        
        """
        _io.write_deploy(deploy, fpath, force)
