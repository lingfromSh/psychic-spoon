import time
from datetime import timedelta

import pytest

from src.backends import RedisBackend
from src.key import Key
from src.types import Integer, Set


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


@pytest.fixture
def role_ids_of_user_cache():
    return Key(
        pattern="user:{user_id}:roles",
        data_type=Set(base_type=Integer()),
        backend=RedisBackend("127.0.0.1", 6379, 0),
    )


def test_set_type_get(redis_client, role_ids_of_user_cache):
    redis_client.sadd("user:1:roles", 1, 2, 3)
    key = role_ids_of_user_cache.build_key(user_id=1)
    assert role_ids_of_user_cache.get(key) == {1, 2, 3}


def test_set_type_mget(redis_client, role_ids_of_user_cache):
    for i in range(100):
        redis_client.sadd(f"user:{i + 1}:roles", *range(i, i + 10))

    keys = [role_ids_of_user_cache.build_key(user_id=i + 1) for i in range(100)]
    assert role_ids_of_user_cache.mget(*keys) == [
        set(range(i, i + 10)) for i in range(100)
    ]


def test_set_type_delete(redis_client, role_ids_of_user_cache):
    raw_keys = [f"user:{i + 1}:roles" for i in range(100)]
    assert redis_client.exists(*raw_keys) != 0

    for i in range(50):
        key = role_ids_of_user_cache.build_key(user_id=i + 1)
        role_ids_of_user_cache.delete(key)

    keys = [role_ids_of_user_cache.build_key(user_id=i) for i in range(50, 101)]
    role_ids_of_user_cache.delete(*keys)

    assert redis_client.exists(*raw_keys) == 0


def test_set_type_set(redis_client, role_ids_of_user_cache):
    key = role_ids_of_user_cache.build_key(user_id=1)
    role_ids_of_user_cache.set(key=key, value={1, 2, 3}, ttl=timedelta(seconds=5))

    assert redis_client.smembers("user:1:roles") == {b"1", b"2", b"3"}
    time.sleep(6)  # wait for ttl
    assert redis_client.get("user:1:roles") is None


def test_set_type_add(redis_client, role_ids_of_user_cache):
    redis_client.sadd("user:1:roles", 1)
    key = role_ids_of_user_cache.build_key(user_id=1)
    role_ids_of_user_cache.add(key, 1, 2, 3)

    assert redis_client.smembers("user:1:roles") == {b"1", b"2", b"3"}


def test_set_type_union(redis_client, role_ids_of_user_cache):
    roles_of_user1 = {1, 2, 3, 4, 5}
    roles_of_user2 = {2, 3, 4, 6, 7, 8}
    redis_client.sadd("user:1:roles", *roles_of_user1)
    redis_client.sadd("user:2:roles", *roles_of_user2)

    key1 = role_ids_of_user_cache.build_key(user_id=1)
    key2 = role_ids_of_user_cache.build_key(user_id=2)
    assert role_ids_of_user_cache.union(key1, key2) == roles_of_user1.union(
        roles_of_user2
    )


def test_set_type_intersection(redis_client, role_ids_of_user_cache):
    roles_of_user1 = {1, 2, 3, 4, 5}
    roles_of_user2 = {2, 3, 4, 6, 7, 8}
    redis_client.sadd("user:1:roles", *roles_of_user1)
    redis_client.sadd("user:2:roles", *roles_of_user2)

    key1 = role_ids_of_user_cache.build_key(user_id=1)
    key2 = role_ids_of_user_cache.build_key(user_id=2)
    assert role_ids_of_user_cache.intersection(
        key1, key2
    ) == roles_of_user1.intersection(roles_of_user2)


def test_set_type_remove(redis_client, role_ids_of_user_cache):
    roles_of_user1 = {1, 2, 3, 4, 5}
    redis_client.sadd("user:1:roles", *roles_of_user1)

    key = role_ids_of_user_cache.build_key(user_id=1)
    assert role_ids_of_user_cache.remove(key, 1, 2, 3) == 3
    assert role_ids_of_user_cache.get(key) == {4, 5}
