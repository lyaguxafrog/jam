---
title: Deprecated methods
---

<!--Everything is relevant 👌-->

- `jam.Jam.jwt_make_payload`: The JWT specification has been introduced, so signing is now done via JWS
- `jam.jwt.JWT`: Use `jam.jose.JWT`
