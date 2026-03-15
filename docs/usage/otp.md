---
title: OTP
---


## Use in instance

### Configuration

Args:

* `type`: `str` - `totp` for TOTP, `hotp` for HOTP.
* `digits`: `int` - Number of digits for the OTP code.
* `digest`: `str` - Hash algorithm to use for the OTP code.
* `interval`: `int` - Interval in seconds for TOTP codes.

Example:

```toml
[jam.otp]
type = "totp"
digits = 6
digest = "sha256"
interval = 30
```

### Usage

#### Get code

Method: `jam.otp_code`

Args:

* `secret`: `str` - Secret key for the OTP code.
* `factor`: `int | None = None` - Factor for HOTP codes. Defaults to `None` for TOTP codes.

Returns:

`str` - Code

```python
code = jam.otp_code(
    secret="CCCUULFTIG5YMEX3HMNHEDCLFM"
)
print(code)
>>> 379982
```

#### Gen OTP uri

Method: `jam.otp_uri`

Args:

* `secret`: `str` - Secret key for the OTP code.
* `name`: `str` - Account name.
* `issuer`: `str` - Issuer for the OTP code.
* `counter`: `int | None = None` - Counter for HOTP codes. Defaults to `None` for TOTP codes.

Returns:

`str` - URI.

```python
uri = jam.otp_uri(
    secret="CCCUULFTIG5YMEX3HMNHEDCLFM",
    issuer="MyApp",
    name="user@example.com"
)
print(uri)
>>> otpauth://totp/MyApp%3Auser%40example.com?secret=CCCUULFTIG5YMEX3HMNHEDCLFM&issuer=MyApp&algorithm=SHA256&digits=6
```

#### Verify code

Method: `jam.otp_verify_code`

Args:

* `secret`: `str` - Secret key for the OTP code.
* `code`: `str` - OTP code to verify.
* `factor`: `int | None = None` - Factor for HOTP codes. Defaults to `None` for TOTP codes.
* `look_ahead`: `int = 1` - Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is `1`.

Returns:

`bool` - Whether the code is valid.

```python
valid = jam.otp_verify_code(
    secret="CCCUULFTIG5YMEX3HMNHEDCLFM",
    code="379982"
)
print(valid)
>>> True
```

## Use out of instance

Modules:

* `jam.otp.TOTP`
* `jam.otp.HOTP`

### TOTP

#### Built

Module: `jam.otp.TOTP`

Args:

* `secret`: `str | bytes` - TOTP Secret.
* `digits`: `int = 6` - Number of digits for the OTP code. Defaults to `6`.
* `algorithm`: `str = "sha1"` - Algorithm for the OTP code. Defaults to `"sha1"`.
* `interval`: `int = 30` - Interval for TOTP codes in seconds. Defaults to `30`.

```python
from jam.otp import TOTP

totp = TOTP(
    secret="CCCUULFTIG5YMEX3HMNHEDCLFM",
    digits=6,
    algorithm="sha1",
    interval=30,
)
```

#### Usage

##### Current code

Method: `totp.now`

Returns: `str` - Current OTP code.

```python
code = totp.now
print(code)
>>> 867877
```

##### Code for specified time

Method: `totp.at`

Args:

* `factor`: `int | None = Non` - Time in UNIX seconds.

Returns:

`str` - OTP code for the specified time.

```python
code = totp.at(factor=None)
print(code)
>>> 867877
```

##### Verify code

Method: `totp.verify`

Args:

* `code`: `str` - OTP code to verify.
* `factor`: `int | None = None` - Factor for HOTP codes. Defaults to `None` for TOTP codes.
* `look_ahead`: `int = 1` - Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is `1`.

Returns:

`bool` - Whether the code is valid.

```python
valid = totp.verify(code="379982")
print(valid)
>>> True
```

### HOTP

#### Built

Module: `jam.otp.HOTP`

Args:

* `secret`: `str` - HOTP Secret.
* `digits`: `int = 6` - Number of digits for the OTP code. Defaults to `6`.
* `digest`: `str = "sha1"` - Algorithm for the OTP code. Defaults to `"sha1"`.

```python
from jam.otp import HOTP

hotp = HOTP(
    secret="CCCUULFTIG5YMEX3HMNHEDCLFM",
    digits=6,
    digest="sha1",
)
```

#### Usage

##### Get code

Method `hotp.at`

Args:

* `factor`: `int` - Counter value for HOTP codes.

Returns:

`str` - Code

```python
code = hotp.at(
    factor=1
)
print(code)
>>> 989760
```

##### Verify code

Method: `hotp.verify`

Args:

* `code`: `str` - OTP code to verify.
* `factor`: `int | None = None` - Counter value for HOTP codes. Defaults to `None` for TOTP codes.
* `look_ahead`: `int = 1` - Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is `1`.

Returns:

`bool` - Whether the code is valid.

```python
valid = hotp.verify(code="379982", factor=1)
print(valid)
>>> True
```
