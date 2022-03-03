import pytest

from psychic_spoon.key import Key


@pytest.fixture(scope="session")
def redis_client():
    from redis import Redis

    return Redis()


def test_redis_string_backend(redis_client):
    from psychic_spoon.backends.redis_backend import RedisStringBackend
    from psychic_spoon.types.string import String

    redis_client.set("user:1", "data")

    backend = RedisStringBackend(host="localhost")
    k = Key(pattern="user:{id}", datatype=String, backend=backend)
    key = k.build_key(id=1)
    assert k.get(key) == "data"

    k.set(key, "new data")
    assert redis_client.get("user:1") == b"new data"
