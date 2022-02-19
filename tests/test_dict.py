import orjson
import pytest
from redis import StrictRedis

from src.backends import RedisBackend
from src.key import Key
from src.types import Dict


@pytest.fixture
def redis_client():
    return StrictRedis()


@pytest.fixture
def user_cache():
    return Key(
        "user:{user_id}",
        data_type=Dict(),
        backend=RedisBackend("127.0.0.1", port=6379, db=0),
    )


def test_dict_type_get(redis_client, user_cache):
    redis_client.set(
        "user:1",
        orjson.dumps({"id": 1, "name": "Stephen.Ling", "gender": "male", "age": 11}),
    )

    key = user_cache.build_key(user_id=1)
    assert user_cache.get(key) == {
        "id": 1,
        "name": "Stephen.Ling",
        "gender": "male",
        "age": 11,
    }


def test_dict_type_delete(redis_client, user_cache):
    key = user_cache.build_key(user_id=1)
    user_cache.delete(key)
    assert redis_client.exists(key) == 0
