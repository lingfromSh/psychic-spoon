import pytest

from src.backends import RedisBackend
from src.key import Key
from src.types import String


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


def test_string_type_get(redis_client):
    redis_client.set("user:1:name", "Stephen.Ling")

    name_of_user_cache = Key(
        pattern="user:{user_id}:name",
        data_type=String(),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )
    key = name_of_user_cache.build_key(user_id=1)
    assert name_of_user_cache.get(key) is not None
