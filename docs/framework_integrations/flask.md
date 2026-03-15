---
title: Jam + Flask = <3
---

# Flask integration

Integration with Flask is done in the form of extension classes, which are [recommended in the official documentation](https://flask.palletsprojects.com/en/stable/extensiondev/).

## How it works

Jam extensions for Flask check requests for the presence of a token in cookies or the header (depending on the settings) and store the data in `flask.g`

Example:

```python
from flask import Flask, g, jsonify

from jam.ext.flask import JWTExtension # For example


app = Flask(__name__)
jwt_ext = JWTExtension(
    config="config.toml",
    header_name="Authorization"
)
jwt_ext.init_app(app)

@app.post("/login")
def login():
    
    # some auth logic
    
    jwt = g.jwt # <- get JWT instance from flask.g
    token = jwt.encode({"username": username})
    return jsonify({"token": token})

@app.get("/profile")
def get_profile():
    payload = g.payload # <- get token payload from flask.g
    if payload:
        return jsonify(payload)
    else:
        return jsonify({"error": "Unauthorized"}), 401
```

## Setup extension

The extension is installed by passing your app to `.init_app`:

```python
from flask import Flask
from jam.ext.flask import SessionExtension  # for example

app = Flask(__name__)
session_extensions = SessionExtension(
    config="config.toml",
    cookie_name="sessionId"
)
session_extensions.init_app(app)
```

## JWT Extension

Module: `jam.ext.flask.JWTExtension`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer
* `cookie_name`: `str | None = None` - Cookie to check
* `header_name`: `str | None = None` - Header to check
* `use_list`: `bool = False` - Use token black/white list
* `bearer`: `bool = True` - Set `Bearer` to header

```python
from flask import Flask
from jam.ext.flask import JWTExtension

app = Flask(__name__)
jwt_ext = JWTExtension(
    config="config.toml",
    header_name="Authorization",
    bearer=True
)
jwt_ext.init_app(app)
```

## PASETO Extension

Module: `jam.ext.flask.PASETOExtension`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer
* `cookie_name`: `str | None = None` - Cookie to check
* `header_name`: `str | None = None` - Header to check
* `bearer`: `bool = True` - Set `Bearer` to header

```python
from flask import Flask
from jam.ext.flask import PASETOExtension

app = Flask(__name__)
paseto_ext = PASETOExtension(
    config="config.toml",
    header_name="Authorization",
    bearer=True
)
paseto_ext.init_app(app)
```

## Server side sessions extension

Module: `jam.ext.flask.SessionExtension`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer
* `cookie_name`: `str | None = None` - Cookie to check
* `header_name`: `str | None = None` - Header to check
* `bearer`: `bool = True` - Set `Bearer` to header

```python
from flask import Flask
from jam.ext.flask import SessionExtension

app = Flask(__name__)
session_ext = SessionExtension(
    config="config.toml",
    header_name="Authorization",
    bearer=True
)
session_ext.init_app(app)
```

## OAuth2 extension

Module: `jam.ext.flask.OAuth2Extension`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer

```python
from flask import Flask
from jam.ext.flask import OAuth2Extension

app = Flask(__name__)
oauth_ext = OAuth2Extension(
    config="config.toml",
)
oauth_ext.init_app(app)
```
