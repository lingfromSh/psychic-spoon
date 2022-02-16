import decimal
import time
from datetime import timedelta

import pytest

from src.backends import RedisBackend
from src.key import Key
from src.types import Decimal


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


@pytest.fixture
def paid_of_user_cache():
    return Key(
        pattern="user:{user_id}:paid",
        data_type=Decimal(),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )


def test_decimal_type_get(redis_client, paid_of_user_cache):
    redis_client.set("user:1:paid", 1.1)
    key = paid_of_user_cache.build_key(user_id=1)
    assert paid_of_user_cache.get(key) == decimal.Decimal("1.1")


def test_decimal_type_mget(redis_client, paid_of_user_cache):
    for i in range(100):
        redis_client.set(f"user:{i + 1}:paid", i + 1)

    keys = [paid_of_user_cache.build_key(user_id=i + 1) for i in range(100)]
    assert paid_of_user_cache.mget(keys=keys) == {
        f"user:{i + 1}:paid": decimal.Decimal(f"{i + 1}") for i in range(100)
    }


def test_decimal_type_delete(redis_client, paid_of_user_cache):
    raw_keys = [f"user:{i + 1}:paid" for i in range(100)]
    assert redis_client.exists(*raw_keys) != 0

    for i in range(50):
        key = paid_of_user_cache.build_key(user_id=i + 1)
        paid_of_user_cache.delete(key)

    keys = [paid_of_user_cache.build_key(user_id=i) for i in range(50, 101)]
    paid_of_user_cache.delete(*keys)

    assert redis_client.exists(*raw_keys) == 0


def test_decimal_type_add(redis_client, paid_of_user_cache):
    key = paid_of_user_cache.build_key(user_id=1)
    paid_of_user_cache.add(
        key=key, data=decimal.Decimal("11.111"), ttl=timedelta(seconds=5)
    )

    assert redis_client.get("user:1:paid").decode() == "11.111"
    time.sleep(6)  # wait for ttl
    assert redis_client.get("user:1:paid") is None


def test_decimal_type_plus(redis_client, paid_of_user_cache):
    key = paid_of_user_cache.build_key(user_id=1)
    paid_of_user_cache.add(key=key, data=decimal.Decimal("11.1111"))

    assert redis_client.get("user:1:paid").decode() == "11.1111"
    paid_of_user_cache.plus(key, 10)
    assert redis_client.get("user:1:paid").decode() == "21.1111"


def test_decimal_type_subtract(redis_client, paid_of_user_cache):
    key = paid_of_user_cache.build_key(user_id=1)
    paid_of_user_cache.add(key=key, data=decimal.Decimal("1.0"))

    assert redis_client.get("user:1:paid").decode() == "1.0"
    paid_of_user_cache.subtract(key, 10)
    assert redis_client.get("user:1:paid").decode() == "-9.0"
