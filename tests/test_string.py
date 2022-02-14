import pytest

from src.key import Key
from src.types import String


@pytest.fixture
def UserCache():
    from redis import StrictRedis

    r_client = StrictRedis(host="127.0.0.1", port=6379, db=0)
    r_client.set("user:1", "a")
    r_client.set("user:2", "b")
    r_client.set("user:3", "c")
    return Key("user:{user_id}", data_type=String())


def test_string_type_get(UserCache):
    user1 = UserCache.get(user_id=1)
    user2 = UserCache.get(user_id=2)
    user3 = UserCache.get(user_id=3)
    assert user1 is not None
    assert user2 is not None
    assert user3 is not None
    assert user1 == "a"
    assert user2 == "b"
    assert user3 == "c"


def test_string_type_mget(UserCache):
    users = UserCache.mget(
        key_mappings=[{"user_id": 1}, {"user_id": 2}, {"user_id": 3}]
    )
    assert users == {"user:1": "a", "user:2": "b", "user:3": "c"}


def test_string_type_add(UserCache):
    UserCache.add(key_mapping={"user_id": 4}, data="d")
    UserCache.add(key_mapping={"user_id": 5}, data="e")
    UserCache.bulk_add(
        mappings=[
            {"key_mapping": {"user_id": 6}, "data": "f"},
            {"key_mapping": {"user_id": 7}, "data": "g"},
            {"key_mapping": {"user_id": 8}, "data": "h"},
        ]
    )

    assert UserCache.get(user_id=4) == "d"
    assert UserCache.get(user_id=5) == "e"
    assert UserCache.get(user_id=6) == "f"
    assert UserCache.get(user_id=7) == "g"
    assert UserCache.get(user_id=8) == "h"


def test_string_type_delete(UserCache):
    UserCache.delete(*[dict(user_id=i) for i in range(1, 9)])

    assert UserCache.mget(key_mappings=[dict(user_id=i) for i in range(1, 9)]) == {
        f"user:{i}": None for i in range(1, 9)
    }
