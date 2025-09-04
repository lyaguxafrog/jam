# Configure OTP

You need to write the configuration in your config file. Since OTP is most often the second
factor for authorization, in Jam, the OTP setting complements the main authorization configuration.
The configuration is set in the `jam.otp` block:

## Params

### `type`: str
OTP type: `hotp` or `otp`.

### `digits`: int
Number of characters in the code.

### `digest`: str
Hash type: `sha1` / `sha256` / `sha512`.

### `interval`: int | None
Code regeneration interval for TOTP.


## Example `yml` config:
```yaml
jam:
  # JWT auth for example
  auth_type: jwt
  secret_key: "SECRET_KEY"
  expire: 3600
  otp:
    type: "totp"  # or hotp
    digits: 6
    digest: sha1
    interval: 30  # only for TOTP
```