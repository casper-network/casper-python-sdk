import datetime
import pytest



@pytest.fixture(scope="session")
def a_test_timestamp() -> int:
    """Returns a test timestamp. 
    
    """
    return datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
