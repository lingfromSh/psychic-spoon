import pytest
from faker import Faker

from src.key import Key
from src.types import Set

faker = Faker()


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis(host="127.0.0.1", port=6379, db=0)


@pytest.fixture
def role_ids_bound_with_user():
    return Key("user:{user_id}:role_ids", data_type=Set())
