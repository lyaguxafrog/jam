# Jam

## Instance

```python
from jam import Jam

jam = Jam(config=config)
```

## Gen payload

You can either create the payload yourself and pass it to kwargs or use `make_payload`.
```python
jam.make_payload(**{"user_id": 1, "role": "admin"})

# or if you need to specify a different exp, e.g. for access token
jam.make_payload(exp=600, **{"user_id": 1})
```
The settings from config will be passed to payload.

## Gen jwt token

```python
token = jam.gen_jwt_token(payload)
```
and you'll receive a JWT token with your payload.

## Verify jwt token

```python
jam.verify_jwt_token(
    token=my_token,
    check_exp=True,
    check_list=False
)
```

If everything went well you just get your payload, if the keys didn't match then raise errors.
(see [API](../api/instance.md#jam.instance.Jam.verify_jwt_token))

### `check_exp`
If we specify this flag, we check the same way, for the lifetime of the token.

### `check_list`
If you specify this flag, we do a check for sheets, see [Jam lists documentation](lists/what.md).