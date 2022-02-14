import json
from dataclasses import dataclass

import factory
import pytest
from faker import Faker
from faker.providers import address, person
from pytest_factoryboy import register

from src.key import Key
from src.types import JSON

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
def fixture():
    from redis import StrictRedis

    user1 = UserFactory.create().__dict__
    user2 = UserFactory.create().__dict__
    user3 = UserFactory.create().__dict__

    r_client = StrictRedis(host="127.0.0.1", port=6379, db=0)
    r_client.set("user:1", json.dumps(user1))
    r_client.set("user:2", json.dumps(user2))
    r_client.set("user:3", json.dumps(user3))
    return Key("user:{user_id}", data_type=JSON()), user1, user2, user3


def test_json_type_get(fixture):
    UserCache, user1, user2, user3 = fixture
    u1 = UserCache.get(user_id=1)
    u2 = UserCache.get(user_id=2)
    u3 = UserCache.get(user_id=3)
    assert u1 == user1
    assert u2 == user2
    assert u3 == user3
