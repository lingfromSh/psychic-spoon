import pytest
from decimal import Decimal as PyDecimal
from faker import Faker

from src.key import Key
from src.types import Integer, Float, Decimal

faker = Faker()


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis(host="127.0.0.1", port=6379, db=0)


def test_number_type_get(redis_client):
    user_age_cache = Key("user:{user_id}:age", data_type=Integer())
    redis_client.set("user:1:age", 11)
    assert user_age_cache.get(user_id=1) == 11 and isinstance(
        user_age_cache.get(user_id=1), int
    )

    user_age_cache = Key("user:{user_id}:age", data_type=Float())
    redis_client.set("user:2:age", 11.1)
    assert user_age_cache.get(user_id=2) == 11.1 and isinstance(
        user_age_cache.get(user_id=2), float
    )

    user_age_cache = Key("user:{user_id}:age", data_type=Decimal())
    redis_client.set("user:3:age", PyDecimal("11.1").to_eng_string())
    assert user_age_cache.get(user_id=3) == PyDecimal("11.1") and isinstance(
        user_age_cache.get(user_id=3), PyDecimal
    )

    user_age_cache = Key("user:{user_id}:age", data_type=Decimal())
    assert list(
        user_age_cache.mget(
            key_params_list=[{"user_id": 1}, {"user_id": 2}, {"user_id": 3}]
        ).values()
    ) == [PyDecimal("11"), PyDecimal("11.1"), PyDecimal("11.1")]


def test_number_type_add(redis_client):
    user_age_cache = Key("user:{user_id}:age", data_type=Integer())
    user_age_cache.add(key_params={"user_id": 1}, data=11)
    assert redis_client.get("user:1:age").decode() == "11"

    user_age_cache = Key("user:{user_id}:age", data_type=Float())
    user_age_cache.add(key_params={"user_id": 2}, data=11.1)
    assert redis_client.get("user:2:age").decode() == "11.1"

    user_age_cache = Key("user:{user_id}:age", data_type=Decimal())
    user_age_cache.add(key_params={"user_id": 3}, data=PyDecimal("11.1"))
    assert redis_client.get("user:3:age").decode() == "11.1"

    user_age_cache.bulk_add(
        key_param_data_mapping_list=[
            {"key_params": {"user_id": i}, "data": PyDecimal(str(i))}
            for i in range(1000)
        ]
    )
    assert [
        item.decode()
        for item in redis_client.mget(keys=[f"user:{i}:age" for i in range(1000)])
    ] == [str(i) for i in range(1000)]


def test_number_type_delete(redis_client):
    redis_client.set("user:1:age", 1)
    redis_client.set("user:2:age", 2)
    redis_client.set("user:3:age", 3)

    user_age_cache = Key("user:{user_id}:age", data_type=Integer())
    user_age_cache.delete({"user_id": 1})
    assert redis_client.get("user:1:age") is None

    user_age_cache = Key("user:{user_id}:age", data_type=Float())
    user_age_cache.delete({"user_id": 2})
    assert redis_client.get("user:2:age") is None

    user_age_cache = Key("user:{user_id}:age", data_type=Decimal())
    user_age_cache.delete({"user_id": 3})
    assert redis_client.get("user:3:age") is None
