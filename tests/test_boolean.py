import pytest
from faker import Faker

from src.key import Key
from src.types import Boolean

faker = Faker()


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis(host="127.0.0.1", port=6379, db=0)


@pytest.fixture
def is_active_user_cache():
    return Key("user:{user_id}:is_active", data_type=Boolean())


def test_boolean_type_get(redis_client, is_active_user_cache):
    redis_client.set("user:1:is_active", "True")
    assert is_active_user_cache.get(user_id=1) is True and isinstance(
        is_active_user_cache.get(user_id=1), bool
    )

    redis_client.set("user:2:is_active", "False")
    assert is_active_user_cache.get(user_id=2) is False and isinstance(
        is_active_user_cache.get(user_id=2), bool
    )

    assert list(
        is_active_user_cache.mget(
            key_params_list=[{"user_id": 1}, {"user_id": 2}]
        ).values()
    ) == [True, False]


def test_boolean_type_add(redis_client, is_active_user_cache):
    is_active_user_cache.add(key_params={"user_id": 1}, data=True)
    assert redis_client.get("user:1:is_active").decode() == "True"

    is_active_user_cache.bulk_add(key_param_data_mapping_list=[{"key_params": {"user_id": 1}, "data": True},
                                                               {"key_params": {"user_id": 2}, "data": False}])
    assert redis_client.get("user:1:is_active").decode() == "True"
    assert redis_client.get("user:2:is_active").decode() == "False"


def test_boolean_type_delete(redis_client, is_active_user_cache):
    is_active_user_cache.delete({"user_id": 1}, {"user_id": 2})
    assert redis_client.mget(keys=["user:1:is_active", "user:2:is_active"]) == [None, None]
