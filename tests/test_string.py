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
