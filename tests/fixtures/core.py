import pytest

import pycspr



@pytest.fixture(scope="session")
def LIB() -> pycspr:
    """Returns pointer to configured library instance. 
    
    """
    return pycspr


@pytest.fixture(scope="session")
def FACTORY():
    """Returns pointer to the library's type factory. 
    
    """    
    return pycspr.factory


@pytest.fixture(scope="session")
def TYPES():
    """Returns pointer to the library's typeset. 
    
    """  
    return pycspr.types
