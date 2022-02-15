import orjson
import pytest
from src.key import Key
from src.types import String
from src.backends import RedisBackend


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis()


def test_string_type_get(redis_client):
    redis_client.set("user:1:name", "Stephen.Ling")
    redis_client.set("user:2:name", orjson.dumps({"name": "Stephen.Ling"}))
    NameOfUserCache = Key(
        pattern="user:{user_id}:name",
        data_type=String(),
        backend=RedisBackend(host="127.0.0.1", port=6379, db=0, password=None),
    )
    assert NameOfUserCache.get(user_id="1") == "Stephen.Ling"
