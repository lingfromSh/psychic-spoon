import time
from datetime import timedelta

import pytest

from src.backends import RedisBackend
from src.key import Key
from src.types import Boolean


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


@pytest.fixture
def name_of_user_cache():
    return Key(
        pattern="user:{user_id}:is_active",
        data_type=Boolean(),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )


def test_boolean_type_get(redis_client, name_of_user_cache):
    redis_client.set("user:1:is_active", "False")
    key = name_of_user_cache.build_key(user_id=1)
    assert name_of_user_cache.get(key) is False


def test_boolean_type_mget(redis_client, name_of_user_cache):
    for i in range(100):
        redis_client.set(f"user:{i + 1}:is_active", "True")

    keys = [name_of_user_cache.build_key(user_id=i + 1) for i in range(100)]
    assert name_of_user_cache.mget(keys=keys) == {
        f"user:{i + 1}:is_active": True for i in range(100)
    }


def test_boolean_type_delete(redis_client, name_of_user_cache):
    raw_keys = [f"user:{i + 1}:is_active" for i in range(100)]
    assert redis_client.exists(*raw_keys) != 0

    for i in range(50):
        key = name_of_user_cache.build_key(user_id=i + 1)
        name_of_user_cache.delete(key)

    keys = [name_of_user_cache.build_key(user_id=i) for i in range(50, 101)]
    name_of_user_cache.delete(*keys)

    assert redis_client.exists(*raw_keys) == 0


def test_boolean_type_add(redis_client, name_of_user_cache):
    key = name_of_user_cache.build_key(user_id=1)
    name_of_user_cache.add(key=key, data=False, ttl=timedelta(seconds=5))

    assert redis_client.get("user:1:is_active").decode() == "False"
    time.sleep(6)  # wait for ttl
    assert redis_client.get("user:1:is_active") is None
