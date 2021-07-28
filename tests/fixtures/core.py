import pytest

import pycspr



@pytest.fixture(scope="session")
def TYPES():
    """Returns pointer to the library's typeset. 
    
    """  
    return pycspr.types
