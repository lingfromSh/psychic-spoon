import json
from dataclasses import dataclass

import factory
import pytest
from faker import Faker
from faker.providers import address, person
from pytest_factoryboy import register

from src.key import Key
from src.types import Dict

faker = Faker()
faker.add_provider(address)
faker.add_provider(person)


@dataclass
class User:
    first_name: str
    last_name: str
    address: str


@register
class UserFactory(factory.Factory):
    first_name = faker.first_name()
    last_name = faker.last_name()
    address = faker.address()

    class Meta:
        model = User


@pytest.fixture
def redis_client():
    from redis import StrictRedis

    return StrictRedis(host="127.0.0.1", port=6379, db=0)


@pytest.fixture
def fixture(redis_client):
    user1 = UserFactory.create().__dict__
    user2 = UserFactory.create().__dict__
    user3 = UserFactory.create().__dict__

    redis_client.set("user:1", json.dumps(user1))
    redis_client.set("user:2", json.dumps(user2))
    redis_client.set("user:3", json.dumps(user3))
    return Key("user:{user_id}", data_type=Dict()), user1, user2, user3


def test_dict_type_get(fixture):
    UserCache, user1, user2, user3 = fixture
    u1 = UserCache.get(user_id=1)
    u2 = UserCache.get(user_id=2)
    u3 = UserCache.get(user_id=3)
    assert u1 == user1
    assert u2 == user2
    assert u3 == user3


def test_dict_type_mget(fixture):
    UserCache, user1, user2, user3 = fixture
    users = UserCache.mget(key_params_list=[{"user_id": i} for i in range(1, 4)])
    assert list(users.values()) == [user1, user2, user3]


def test_dict_type_add(redis_client, fixture):
    UserCache = fixture[0]
    random_user = UserFactory.create().__dict__
    UserCache.add(key_params={"user_id": 4}, data=random_user)
    assert json.loads(redis_client.get("user:4").decode()) == random_user

    UserCache.bulk_add(
        key_param_data_mapping_list=[
            {"key_params": {"user_id": 6}, "data": random_user},
            {"key_params": {"user_id": 7}, "data": random_user},
            {"key_params": {"user_id": 8}, "data": random_user},
        ]
    )

    assert [
               json.loads(item)
               for item in redis_client.mget(keys=[f"user:{i}" for i in range(6, 9)])
           ] == [random_user] * 3


def test_dict_type_delete(redis_client, fixture):
    UserCache = fixture[0]

    UserCache.delete(*[
        {
            "user_id": i
        }
        for i in range(1, 9)
    ])

    assert len(redis_client.keys("user:")) == 0
