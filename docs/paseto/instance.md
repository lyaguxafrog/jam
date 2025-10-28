# Jam PASETO

## Instance

```python
from jam import Jam

jam = Jam(config=config)
```

## Gen payload
```python
payload = jam.paseto_make_payload(
    expire=3600,
    **{"sub": 1, "role": "user"}
)
```
### `expire`: `int`
Token lifetime

### **`data`: `dict[str, Any]`
Payload with data

## Generate token
```python
token = jam.paseto_create(
    payload={"sub": 1},  # or payload from jam.paseto_make_payload
    footer="custom string, dict[str, Any] or None"
)
```
### `payload`: `dict[str, Any]`
Token payload

### `footer`: `dict[str, Any] | str | None`
Token footer


## Decode token
```python
decoded_data = jam.paseto_decode(
    token=token,
    check_exp=True,
    check_list=True
)

print(decoded_data)  # {"payload": ..., "footer": ...}
```
### `token`: `str`
Encoded token

### `check_exp`: `bool`
Checking the token lifetime.
`jam.Jam` and `jam.aio.Jam` check the `exp` field in the payload.

### `check_list`: `bool`
Not realised