import time
from datetime import timedelta

import pytest

from src.backends import RedisBackend
from src.key import Key
from src.types import Integer


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


@pytest.fixture
def login_count_of_user_cache():
    return Key(
        pattern="user:{user_id}:login:count",
        data_type=Integer(),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )


def test_integer_type_get(redis_client, login_count_of_user_cache):
    redis_client.set("user:1:login:count", 0)
    key = login_count_of_user_cache.build_key(user_id=1)
    assert login_count_of_user_cache.get(key) == 0


def test_integer_type_mget(redis_client, login_count_of_user_cache):
    for i in range(100):
        redis_client.set(f"user:{i + 1}:login:count", f"{i + 1}")

    keys = [login_count_of_user_cache.build_key(user_id=i + 1) for i in range(100)]
    assert login_count_of_user_cache.mget(*keys) == [i + 1 for i in range(100)]


def test_integer_type_delete(redis_client, login_count_of_user_cache):
    raw_keys = [f"user:{i + 1}:login:count" for i in range(100)]
    assert redis_client.exists(*raw_keys) != 0

    for i in range(50):
        key = login_count_of_user_cache.build_key(user_id=i + 1)
        login_count_of_user_cache.delete(key)

    keys = [login_count_of_user_cache.build_key(user_id=i) for i in range(50, 101)]
    login_count_of_user_cache.delete(*keys)

    assert redis_client.exists(*raw_keys) == 0


def test_integer_type_add(redis_client, login_count_of_user_cache):
    key = login_count_of_user_cache.build_key(user_id=1)
    login_count_of_user_cache.set(key=key, value=1, ttl=timedelta(seconds=5))

    assert redis_client.get("user:1:login:count").decode() == "1"
    time.sleep(6)  # wait for ttl
    assert redis_client.get("user:1:login:count") is None


def test_integer_type_plus(redis_client, login_count_of_user_cache):
    key = login_count_of_user_cache.build_key(user_id=1)
    login_count_of_user_cache.set(key=key, value=1)

    assert redis_client.get("user:1:login:count").decode() == "1"
    login_count_of_user_cache.plus(key, 10)
    assert redis_client.get("user:1:login:count").decode() == "11"


def test_integer_type_subtract(redis_client, login_count_of_user_cache):
    key = login_count_of_user_cache.build_key(user_id=1)
    login_count_of_user_cache.set(key=key, value=1)

    assert redis_client.get("user:1:login:count").decode() == "1"
    login_count_of_user_cache.subtract(key, 10)
    assert redis_client.get("user:1:login:count").decode() == "-9"
