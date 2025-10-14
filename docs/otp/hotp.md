# How to use HOTP

After [configuration](/otp/config), HOTP will be available through the main instance:

```python

from jam import Jam

jam = Jam(config=config)

code = jam.otp_code(
    secret="USERSECRETKEY",
    factor=1  # A counter is used as a factor in HOTP
)
```
!!! tip
    In OTP, you need to use the **secret specifically for each user and store it securely.**
    You can use: [`jam.utils.generate_otp_key`](/api/utils/otp_keys/).
    We may develop a mechanism for encrypting secrets in the future, but we are not yet sure if there is a demand for it.

## Verify code

```python
result: bool = jam.otp_verify_code(
    secret="USERSECRETKEY",
    code="123456",
    factor=counter,
    look_ahead=1
)
```

## Gen URI for auth apps
To make it convenient for users to use your service, it is better to provide
a URI for generating codes that can be used in
Google Authenticator or any other application.

```python
uri = jam.otp_uri(
    secret="USER-SECRET-KEY",
    name="username/email/or-something",
    issuer="your-service-name",
    counter=999
)

print(uri)  # otpauth://hotp/your-service-name%3Ausername?secret=MYSUPERSECRES&issuer=your-service-name&algorithm=SHA1&digits=6&counter=999
```

## Use HOTP out of `jam.Jam`

You can use OTP outside the main instance, for example if your framework provides
convenient authorization mechanisms but does not provide OTP. To do this, you can use `jam.otp.HOTP` directly:
```python
from jam.otp import HOTP

hotp = HOTP(
    secret="somesecretkey",
    digits=6,
    digest="sha1"
)

counter = 0

hotp.at(counter) # 994684
counter += 1
hotp.at(counter)  # 545896

hotp.at(factor=counter)

result: bool = hotp.verify(code="123456", factor=counter, look_ahead=30)
```
