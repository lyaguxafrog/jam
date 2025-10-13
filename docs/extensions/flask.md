---
title: "Jam + Flask = <3"
---

Integration with Flask is done in the form of extension classes,
[which are recommended in the official documentation](https://flask.palletsprojects.com/en/stable/extensiondev/).


## Jam Extension

This is a simple extension that does not check tokens/sessions like `JWTExtension` and `SessionExtension`.
It is needed for easy access to jam inside routes, via `current_app.extensions[“jam”]`:

!!! tip
    For more convenient operation, it is recommended to
    use `JamExtension` in conjunction with another extension, for example `JamExtension` + `JWTExtension`.

```python
from flask import current_app

@app.route("/login")
def login(some_param, some_param2):
    jam = current_app.extensions["jam"]
    # some logic
    token = jam.gen_jwt_token(payload)
```

Example of integration with your Flask application:
```python
from flask import Flask

from jam import Jam
from jam.ext.flask import JamExtension

jam = Jam()

def create_app() -> Flask:
    app = Flask(__name__)
    jam_ext = JamExtension(jam)
    jam_ext.init_app(app)
    return app
```

---
## JWT Extension

This extension checks tokens from the header or cookie
and writes the payload to the [route context](https://flask.palletsprojects.com/en/stable/api/#flask.g).

### Setup extension

#### `jam`: `Jam`
Jam instance.

#### `app`: `Flask | None = None`
Flask app instance.

#### `cookie_name`: `str | None`

The cookie name for the access token. If passed, `Extension` will
read the token from it. If `None` is passed, `Extension` will read the `header`.

#### `header_name`: `str | None`

The name of the header for the access token. If passed, `Extension` will
read the token from the header. If `None` is passed, `Extension` will read the `cookie`.

!!! tip
    `JWTExtension` expects the header to be in the format: `Bearer <token>`

```python
from flask import Flask

from jam import Jam
from jam.ext.flask import JWTExtension


app = Flask(__name__)
jam = Jam()
jwt_ext = JWTExtension(jam, header_name="Authorization", cookie_name=None)
jwt_ext.init_app(app)
```

### Usage example

```python
from flask import Flask, g, request, Response, abort

from jam import Jam
from jam.ext.flask import JWTExtension

app = Flask(__name__)
jam = Jam()
jwt_ext = JWTExtension(jam, header_name='Authorization', cookie_name=None)
jwt_ext.init_app(app)


@app.route("/login")
def login(username, password) -> Response:
    # some logic
    payload = jam.make_payload(**{"user": 1})
    token = jam.gen_jwt_token(payload)
    response = Response(token)
    return response


@app.route("/get_user")
def get_user() -> Response:
    payload = g.payload
    if not payload:
        abort(403)
    response = Response(payload)
    return response
```

---
## Session Extension

This extension checks sessions ids from the header or cookie
and writes the payload to the [route context](https://flask.palletsprojects.com/en/stable/api/#flask.g).

### Setup extension

#### `jam`: `Jam`
Jam instance.

#### `app`: `Flask | None = None`
Flask app instance.

#### `cookie_name`: `str | None`

The cookie name for the session id. If passed, `Extension` will
read the session id from it. If `None` is passed, `Extension` will read the `header`.

#### `header_name`: `str | None`

The name of the header for the session id. If passed, `Extension` will
read the session id from the header. If `None` is passed, `Extension` will read the `cookie`.

!!! tip
    `SessionExtension` expects the header to be in the format: `Bearer <token>`



```python
from flask import Flask

from jam import Jam
from jam.ext.flask import SessionExtension


app = Flask(__name__)
jam = Jam()
session_ext = SessionExtension(jam, header_name=None, cookie_name="sessionId")
session_ext.init_app(app)
```

### Usage example
```python
from flask import Flask, g, request, Response, abort

from jam import Jam
from jam.ext.flask import SessionExtension

app = Flask(__name__)
jam = Jam()
session_ext = SessionExtension(jam, header_name=None, cookie_name="sessionId")
session_ext.init_app(app)


@app.route("/login")
def login(username, password) -> Response:
    # some logic
    session_id = jam.create_session("usern", {"user": 1})
    response = Response(session_id)
    response.set_cookie("sessionId", session_id)
    return response


@app.route("/get_user")
def get_user() -> Response:
    payload = g.payload
    if not payload:
        abort(403)
    response = Response(payload)
    return response
```
