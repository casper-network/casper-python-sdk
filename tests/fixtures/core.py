import pytest

import pycspr



@pytest.fixture(scope="session")
def LIB() -> pycspr:
    """Returns pointer to configured library instance. 
    
    """
    return pycspr


@pytest.fixture(scope="session")
def CLIENT(LIB):
    """Returns pointer to a client pointing at NCTL:N1. 
    
    """    
    return LIB.NodeClient(LIB.NodeConnectionInfo(
        host="localhost",
        port_rest=14101,
        port_rpc=11101,
        port_sse=18101
    ))


@pytest.fixture(scope="session")
def FACTORY(LIB):
    """Returns pointer to the library's type factory. 
    
    """    
    return LIB.factory


@pytest.fixture(scope="session")
def TYPES(LIB):
    """Returns pointer to the library's typeset. 
    
    """  
    return LIB.types
