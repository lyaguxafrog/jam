---
title: OAuth2
---

## Use in instance

### Configuration

Args:

* `providers`: `hashmap`
  * `client_id`: `str` - Client ID in your app.
  * `client_secret`: `str` - Client secret in your app.
  * `auth_url`: `str` - Authorization URL.
  * `token_url`: `str` - Token URL.
  * `redirect_uri`: `str` - Redirect URI.

Example:

```toml
[jam.oauth2.providers.linkedin]  # OAuth2 client
client_id = "$LINKEDIN_CLIENT_ID"
client_secret = "$LINKEDIN_CLIENT_SECRET"
auth_url = "https://www.linkedin.com/oauth/v2/authorization"
token_url = "https://www.linkedin.com/oauth/v2/accessToken"
redirect_url = "https://example.com/callback/linkedin"

[jam.oauth2.providers.github]  # builtin providers
client_id = "$GITHUB_CLIENT_ID"
client_secret = "$GITHUB_CLIENT_SECRET"
redirect_url = "https://example.com/callback/github"
```


### Get auth url

Method: `jam.oauth2_get_authorized_url`

Args:

* `provider`: `str` - Provider name from config
* `scope`: `list[str]` - Scope for provider

Returns:

`str`: URL for authoriaztion

```python
url = jam.oauth2_get_authorized_url(
    provider="github",
    scope=["gist"],
#    **extra_params
)
```

### Fetch token

Method: `jam.oauth2_fetch_token`

Args:

* `provider`: `str` - Provider name from config
* `code`: `str` - OAuth2 code
* `grant_type`: `str = authorization_code` - Type of oauth2 grant

Returns:

`dict[str, Any]` - Tokens

```python
tokens = jam.oauth2_fetch_token(
    provider="github",
    code="HGvdskHG",
    grant_type="authorization_code"
)
```
