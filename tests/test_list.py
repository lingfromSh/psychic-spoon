import time
from datetime import timedelta

import pytest
from redis import StrictRedis

from src.backends import RedisBackend
from src.key import Key
from src.types import Integer, List


@pytest.fixture
def redis_client():
    return StrictRedis()


@pytest.fixture
def user_list_of_product():
    return Key(
        "product:{product_id}:users",
        data_type=List(Integer()),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )


def test_list_type_get(redis_client, user_list_of_product):
    redis_client.flushall()
    redis_client.rpush("product:1:users", 1, 2, 3, 4, 5)

    key = user_list_of_product.build_key(product_id=1)
    assert user_list_of_product.get(key=key) == [1, 2, 3, 4, 5]

    for i in range(1, 1000):
        redis_client.rpush(f"product:{i + 1}:users", i + 1, i + 2, i + 3, i + 4, i + 5)

    keys = [user_list_of_product.build_key(product_id=i + 1) for i in range(1000)]
    assert user_list_of_product.mget(*keys) == [
        [i + 1, i + 2, i + 3, i + 4, i + 5] for i in range(1000)
    ]


def test_list_type_set(redis_client, user_list_of_product):
    redis_client.flushall()

    key = user_list_of_product.build_key(product_id=1)
    user_list_of_product.set(key, value=[1, 2, 3, 4, 5], ttl=timedelta(seconds=5))

    assert redis_client.lrange(key, start=0, end=-1) == [b"1", b"2", b"3", b"4", b"5"]
    time.sleep(5)
    assert redis_client.exists(key) == 0
