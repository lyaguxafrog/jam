---
title: Config
---

## Params

### `providers`: `hashmap`
There may be several providers, which are configured according to the following principle:
`"<provider-name>": {<settings>}`

#### `cliend_id`: `str`
Your OAuth2 client ID

#### `client_secret`: `str`
Secret of your OAuth2 client

#### `auth_url`: `str`
URL for obtaining an authorization code. Not used in [built-in clients](builtins.md).

#### `token_url`: `str`
URL for obtaining tokens. Not used in [built-in clients](builtins.md).

#### `redirect_url`: `str`
URL where the user will be redirected with scope and code.

#### `module`: `str`
Path to the module in the format `app.some_modules.MyOAuth2Client`, used only in [custom modules](custom_module.md).

Example:

```yaml
jam:
  auth_type: oauth2
  providers:
  
    linkedin:  # this is a custom OAuth2Client
      client_id: LINKEDIN_CLIENT_ID
      client_secret: LINKEDIN_CLIENT_SECRET
      auth_url: https://www.linkedin.com/oauth/v2/authorization
      token_url: https://www.linkedin.com/oauth/v2/accessToken
      redirect_url: https://example.com/callback/linkedin
  
    github:  # this is a built-in client
      client_id: GITHUB_CLIENT_ID
      client_secret: GITHUB_CLIENT_SECRET
      redirect_url: https://example.com/callback/github

    twitter:  # this is custom module
      module: myapp.auth.TwiiterOauth2
      some_arg: value1
      another_arg: value2
```