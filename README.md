# Psychic Spoon

## Introduction

Cache key management always is a tough task during developing.

Cache a data may involve generating keys, converting data to right struct, assigning expiration, converting raw to
proper python type and handling failures.

The purpose of `Psychic Spoon` is to keep your plenty of cache keys clear.

## Concepts

In KV databases, a key is used as the unique identification to access the value. In practice, keys with the same pattern
are generally designed as a kind of data with the same structure. And Various KV databases almost are same.

Therefore, `Psychic Spoon` provides:

1. a key object to describe key's pattern and data structure.
2. a type object to describe data in python.
3. a backend object to describe how data in python to store in database.

### Key

```python
from psychic_spoon.key import Key
```

### Type

- Boolean
- Dict (support nested)
- Float
- Integer
- List (support nested)
- Set  (support nested)
- String

### Backend

- RedisBackend
    - RedisStringBackend
    - RedisSetBackend

## Usage

For example, we need a redis string to store a user's session dict.

```python
from datetime import timedelta
from psychic_spoon.key import Key
from psychic_spoon.types.dict import Dict
from psychic_spoon.types.integer import Integer
from psychic_spoon.types.set import Set
from psychic_spoon.types.string import String
from psychic_spoon.backends.redis_backend import RedisStringBackend

backend = RedisStringBackend(host="localhost", port=6379)

user_session_cache = Key("user:{id}:session",
                         datatype=Dict(
                             username=String,
                             name=String,
                             age=Integer,
                             roles=Set(Integer),
                             ip_address=Dict(
                                 type=String,
                                 address=String
                             )
                         ),
                         backend=backend,
                         ttl=timedelta(hours=12))

key = user_session_cache.build_key(id=1)
user_dict = {
    "username": "jame-curtis",
    "name": "James Curtis",
    "age": 26,
    "roles": {15, 82, 81},
    "ip_address": {
        "type": "ipv4",
        "address": "192.168.1.1"
    }
}

# Save your cache
user_session_cache.set(key, user_dict)

# Fetch your cache
user_dict = user_session_cache.get(key)

```

## Roadmap

- [ ] An event loop to handling success/failure callback
- [ ] Replace pottery with RedisBackend
- [ ] A method mapping layer between Backend and Type
- [ ] Flexible mapping type and backend
