---
title: Built-in clients
---

Jam has several built-in OAuth2 clients that do not require you to write the API yourself.
Each client is configured in the same way:

```python
config = {
    "auth_type": "oauth2",
    "providers": {
        "<provider_name>": {
            "client_id": "ID",
            "client_secret": "SECRET",
            "redirect_url": "https://example.com"
            # No other parameters are required.
        }
    }
}
```
For more details, see the [configuration documentation](config.md).

## Clients:
### GitHub
Provider name: `github`

[GitHub OAuth2 documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)

### GitLab
Provider name: `gitlab`

[GitLab OAuth2 documentation](https://docs.gitlab.com/api/oauth2/)

### Google
Provider name: `google`

[Google cloud documentation](https://developers.google.com/identity/protocols/oauth2)

### Yandex
Provider name: `yandex`

[Yandex ID documentation](https://yandex.ru/dev/id/doc)