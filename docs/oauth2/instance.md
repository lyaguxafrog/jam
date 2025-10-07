---
title: Jam OAuth2
---

## Instance

```python
from jam import Jam

jam = Jam(config=config)
```

## Get auth URL
Obtaining a URL for authorization.

```python
url = jam.oauth2_get_authorized_url(
    provider="github",
    scope=["gist"],
)
```

### `provider`: `str`
Provider name from [config](config.md).

### `scope`: `list[str]`
The scope is specific to each service; please
check your provider's documentation for details.

### kwargs: `extra_params`
Additional parameters, if needed.

## Fetch token
Exchange code for tokens.

```python
tokens = jam.oauth2_fetch_token(
    provider="github",
    code="some_code",
    grant_type="authorization_code"
)
```

### `provider`: `str`
Provider name from [config](config.md).

### `code`: `str`
Code received after successful authorization.

### `grant_type`: `str` = `"authorization_code"`
OAuth2 grant type.

### kwargs: `extra_params`
Additional parameters, if needed.

## Refresh token
Refresh tokens

```python
new_tokens = jam.oauth2_refresh_token(
    provider="github",
    refresh_token=token,
    grant_type="refresh_token"
)
```

### `provider`: `str`
Provider name from [config](config.md).

### `refresh_token`: `str`
Refresh token

### `grant_type`: `str` = `"refresh_token"`
OAuth2 grant type.

### kwargs: `extra_params`
Additional parameters, if needed.

## Machine to Machine auth
Authorization without user involvement.

```python
tokens = jam.oauth2_client_credentials_flow(
    provider="github",
    scope=["gist"],
)
```

### `provider`: `str`
Provider name from [config](config.md).

### `scope`: `list[str]`
The scope is specific to each service; please
check your provider's documentation for details.

### kwargs: `extra_params`
Additional parameters, if needed.