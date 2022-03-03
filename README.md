# Psychic Spoon

## Introduction

Cache key management always is a tough task during developing.

For example, we need a redis string to store a user's session dict.

```python
# Set one user's session
session_key_pattern = "user:{id}:session"
session_expiration = 60 * 60 * 12  # 12 hours

user_dict = {
    "id": "1eaf0dfc-a324-45c0-8545-1d77260273a2",
    "name": ,
    "age": int
}
redis.set(session_key_pattern.format(id= < user_id >), json.dumps(user_dict), ex = session_expiration)

# Get one user's session
if json_string_session := redis.get(session_key_pattern.format(id= < user_id >)):
    session = json.dumps(json_string_session)
else:
    session = None
```

From this example code, a cache key may involving generating keys, converting data to right struct, assigning
expiration, converting raw to proper python type and handling failures.

So `Psychic Spoon` 's purpose is to keep your plenty of cache keys clear.

## Usage

```python
user_session_key = Key("user:{id}:session",
                       data_type=Dict(),
                       backend=RedisBackend(...),
                       ttl=timedelta(hours=12))

key = user_session_key.build_key(id=1)
user_dict = {
    "id": xxx,
    "name": xxx,
    "last_login": xxx
}
user_session_key.set(key, user_dict)
user_dict = user_session_key.get(key)
```

## Roadmap

- [ ] An event loop to handling success/failure callback
- [ ] Replace pottery with RedisBackend
- [ ] A method mapping layer between Backend and Type
- [ ] Flexible mapping type and backend
