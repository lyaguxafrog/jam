# Configure OTP

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
  otp:
    type: "totp"  # or hotp
    digits: 6
    digest: sha1
    interval: 30  # only for TOTP
```