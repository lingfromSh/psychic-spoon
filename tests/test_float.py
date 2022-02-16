import time
from datetime import timedelta

import pytest

from src.backends import RedisBackend
from src.key import Key
from src.types import Float


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


@pytest.fixture
def score_of_user_cache():
    return Key(
        pattern="user:{user_id}:score",
        data_type=Float(),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )


def test_float_type_get(redis_client, score_of_user_cache):
    redis_client.set("user:1:score", 0.1)
    key = score_of_user_cache.build_key(user_id=1)
    assert score_of_user_cache.get(key) == 0.1


def test_float_type_mget(redis_client, score_of_user_cache):
    for i in range(100):
        redis_client.set(f"user:{i + 1}:score", f"{i + 1}.1")

    keys = [score_of_user_cache.build_key(user_id=i + 1) for i in range(100)]
    assert score_of_user_cache.mget(keys=keys) == {
        f"user:{i + 1}:score": i + 1.1 for i in range(100)
    }


def test_float_type_delete(redis_client, score_of_user_cache):
    raw_keys = [f"user:{i + 1}:score" for i in range(100)]
    assert redis_client.exists(*raw_keys) != 0

    for i in range(50):
        key = score_of_user_cache.build_key(user_id=i + 1)
        score_of_user_cache.delete(key)

    keys = [score_of_user_cache.build_key(user_id=i) for i in range(50, 101)]
    score_of_user_cache.delete(*keys)

    assert redis_client.exists(*raw_keys) == 0


def test_float_type_add(redis_client, score_of_user_cache):
    key = score_of_user_cache.build_key(user_id=1)
    score_of_user_cache.add(key=key, data=1, ttl=timedelta(seconds=5))

    assert redis_client.get("user:1:score").decode() == "1"
    time.sleep(6)  # wait for ttl
    assert redis_client.get("user:1:score") is None


def test_float_type_plus(redis_client, score_of_user_cache):
    key = score_of_user_cache.build_key(user_id=1)
    score_of_user_cache.add(key=key, data=1.1)

    assert redis_client.get("user:1:score").decode() == "1.1"
    score_of_user_cache.plus(key, 10)
    assert redis_client.get("user:1:score").decode() == "11.1"


def test_float_type_subtract(redis_client, score_of_user_cache):
    key = score_of_user_cache.build_key(user_id=1)
    score_of_user_cache.add(key=key, data=1.1)

    assert redis_client.get("user:1:score").decode() == "1.1"
    score_of_user_cache.subtract(key, 10)
    assert redis_client.get("user:1:score").decode() == "-8.9"
