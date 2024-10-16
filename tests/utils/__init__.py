from tests.utils import cctl
from tests.utils import test_data_generator


def assert_entity(entity: object, entity_type: type):
    assert entity is not None and isinstance(entity, entity_type)
