import orjson
import pytest

from psychic_spoon.key import Key


@pytest.fixture(scope="session")
def redis_client():
    from redis import Redis

    return Redis()


def test_redis_string_backend(redis_client):
    from psychic_spoon.backends.redis_backend import RedisStringBackend
    from psychic_spoon.types.boolean import Boolean
    from psychic_spoon.types.dict import Dict
    from psychic_spoon.types.float import Float
    from psychic_spoon.types.integer import Integer
    from psychic_spoon.types.list import List
    from psychic_spoon.types.set import Set
    from psychic_spoon.types.string import String

    backend = RedisStringBackend(host="localhost")

    redis_client.set("user:1", "data")
    k = Key(pattern="user:{id}", datatype=String, backend=backend)
    key = k.build_key(id=1)
    assert k.get(key) == "data"
    k.set(key, "new data")
    assert redis_client.get("user:1") == b"new data"
    k.delete(key)
    assert redis_client.exists(key) == 0

    redis_client.set("user:1:is_active", "True")
    k = Key(pattern="user:{id}:is_active", datatype=Boolean, backend=backend)
    key = k.build_key(id=1)
    assert k.get(key)
    k.delete(key)
    assert redis_client.exists(key) == 0

    redis_client.set("user:1:login_count", 11)
    k = Key(pattern="user:{id}:login_count", datatype=Integer, backend=backend)
    key = k.build_key(id=1)
    assert k.get(key) == 11
    k.set(key, 12)
    assert k.get(key) == 12
    k.delete(key)
    assert redis_client.exists(key) == 0

    redis_client.set("user:1:random", 11.5)
    k = Key(pattern="user:{id}:random", datatype=Float, backend=backend)
    key = k.build_key(id=1)
    assert k.get(key) == 11.5
    k.set(key, 12.5)
    assert k.get(key) == 12.5
    k.set(key, k.get(key) - 1)
    assert k.get(key) == 11.5
    k.set(key, k.get(key))
    assert k.get(key) == 11.5
    k.delete(key)
    assert redis_client.exists(key) == 0

    redis_client.set("user:1", orjson.dumps({"username": "Ling", "age": 26}))
    k = Key("user:{id}", datatype=Dict(username=String, age=Integer), backend=backend)
    key = k.build_key(id=1)
    assert k.get(key) == {"username": "Ling", "age": 26}
    k.set(key, {"username": "StephenLing", "age": 30})
    assert orjson.loads(redis_client.get("user:1")) == {
        "username": "StephenLing",
        "age": 30,
    }
    k.delete(key)
    assert redis_client.exists("user:1") == 0

    redis_client.set("paid", orjson.dumps([1, 2, 3]))
    k = Key("paid", datatype=List(Integer), backend=backend)
    key = k.build_key()
    assert k.get(key) == [1, 2, 3]
    k.set(key, [4, 5, 6])
    assert orjson.loads(redis_client.get("paid")) == [4, 5, 6]
    k.delete(key)
    assert redis_client.exists("paid") == 0

    redis_client.set("paid", orjson.dumps([1, 2, 3]))
    k = Key("paid", datatype=Set(Integer), backend=backend)
    key = k.build_key()
    assert k.get(key) == {1, 2, 3}
    k.set(key, {4, 5, 6})
    assert set(orjson.loads(redis_client.get("paid"))) == {4, 5, 6}
    k.delete(key)
    assert redis_client.exists("paid") == 0
