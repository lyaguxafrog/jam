# How to use TOTP

After [configuration](/otp/config), TOTP will be available through the main instance:

```python

from jam import Jam

jam = Jam(config=config)

code = jam.get_otp_code(
    secret="USERSECRETKEY"
)
```
!!! tip
    In OTP, you need to use the **secret specifically for each user and store it securely.**

## Verify code

```python
result: bool = jam.verify_otp_code(
    secret="USERSECRETKEY",
    code="123456",
    look_ahead=1
)
```

## Gen URI for auth apps
To make it convenient for users to use your service, it is better to provide
a URI for generating codes that can be used in
Google Authenticator or any other application.

```python
uri = jam.get_otp_uri(
    secret="USER-SECRET-KEY",
    name="username/email/or-something",
    issuer="your-service-name",
)

print(uri)  # otpauth://totp/your-service-name%3Ausername?secret=MYSUPERSECRES&issuer=your-service-name&algorithm=SHA1&digits=6
```

## Use TOTP out of `jam.Jam`

You can use OTP outside the main instance, for example if your framework provides
convenient authorization mechanisms but does not provide OTP. To do this, you can use `jam.otp.TOTP` directly:
```python
from jam.otp import TOTP

totp = TOTP(
    secret="somesecretkey",
    digits=6,
    digest="sha1",
    interval=30
)

totp.now  # "775934"
# or for specific time:
totp.at(factor=1756944388)

result: bool = totp.verify(code="123456", look_ahead=30)
```

For more information see [API](/api/otp/totp).