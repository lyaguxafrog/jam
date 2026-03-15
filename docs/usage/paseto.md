---
title: PASETO
---

## Use in instance

### Config

Args:

* `version`: `str` - PASETO version(v1 / v2 / v3 / v4).
* `purpose`: `str` - `local` / `public`.
* `secret_key`: `str | None`: Secret key for PASETO.


```toml
[jam.paseto]
version = "v4"
purpose = "local"
secret_key = "3KVs1nMaWb8jP0_aYMhsRN_hHf9dwV1UdqKk_wUXlnM"
```

### Usage

```python
from jam import Jam

jam = Jam(config="config.toml")
```

#### Generate payload

Method: `jam.paseto_make_payload`

Args:

* `exp`: `int | None = Non`: Token lifetime.
* `data`: `dict[str, Any]`: Data to payload.

Returns:

`dict[str, Any]`: Payload.

```python
payload = jam.paseto_make_payload(
    exp=3600,
    data={
        "id": 1,
        "role": "admin"
    }
)
print(token)
>>> {
        'iat': 1772129106.102009,
        'exp': 1772132706.102009,
        'pit': '0c2c38d2-5dcb-4294-bb2d-0820f6ff787d',
        'data': {'id': 1, 'role': 'admin'}
    }
```

#### Create token

Method: `jam.paset_create`

Args:

* `payload`: `dict[str, Any]` - Token payload.
* `footer`: `dict[str, Any] | str | None` - Token footer.

Returns:

`str`: PASETO.

```python
token = jam.paseto_create(
    payload=payload,
    footer={
        "some": "footer",
        "as": "dict"
    }
)
print(token)
>>> v4.local.wTgWfsaSTjBcuZSqI7mT...
```


#### Decode token

Method: `jam.paseto_decode`

Args:

* `token`: `str` - PASETO.
* `check_exp`: `bool = True` - Check token expiration.
* `check_list`: `bool = True` - Check token list.

Returns:

`dict[str, dict[str, Any] | str | None]` - dict like `{"payload": {<payload_data>}, "footer": <footer_data>`.

```python
data = jam.paseto_decode(
    token=token,
    check_exp=True,
    check_list=False
)
print(data)
>>> {
        'payload': {
            'data': {'id': 1, 'role': 'admin'},
            'exp': 1772132706.102009,
            'iat': 1772129106.102009,
            'pit': '0c2c38d2-5dcb-4294-bb2d-0820f6ff787d'
            },
        'footer': {
            'as': 'dict',
            'some': 'footer'
        }
    }
```

## Use out of instance

Modules:

* `jam.paseto.PASETOv1`
* `jam.paseto.PASETOv2`
* `jam.paseto.PASETOv3`
* `jam.paseto.PASETOv4`

For example, we will show how to work with v4.

### Built

Method: `PASETOv4.key`

Args:

* `purpose`: `str` - `local` / `public`.
* `secret_key`: `str | bytes`: Symmetric key for local and Asymmetric key for public.

Returns:

`PASETOv4`: Built PASETOv4 instance.

```python
from jam.paseto import PASETOv4`

paseto = PASETOv4.key(
    purpose="local",
    secret_key="3KVs1nMaWb8jP0_aYMhsRN_hHf9dwV1UdqKk_wUXlnM"
)
```

### Encode token

Method: `paseto.encode`

Args:

* `payload`: `dict[str, Any]` - Token payload.
* `footer`: `dict[str, Any] | str | None = Non` - Token footer.
* `serializer`: `type[BaseEncoder] | BaseEncoder = JamEncoder` - JSON serializer.

Returns:

`str`: PASETO.

```python
token = paseto.encode(
    payload={"id": 1, "role": "admin"},
    footer="some_footer_as_string"
)
print(token)
>>> v4.local.Py0Y4CbmylrmFo3F54u7l1gZCfd
```

### Decode token

Method: `paseto.decode`

Args:

* `token`: `str` - PASETO token.
* `serializer`: `type[BaseEncoder] | BaseEncoder = JamEncoder` - JSON serializer.

Returns:

`tuple[dict[str, Any], dict[str, Any] | str, | None]` - Decoded payload and footer.

```python
payload, footer = paseto.decode(
    token=token,
    check_exp=True,
    check_list=False
)
print(payload)
>>> {
        'id': 1,
        'role': 'admin'
    }
print(footer)
>>> "some_footer_as_string"
```
