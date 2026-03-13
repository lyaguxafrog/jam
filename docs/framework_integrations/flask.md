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
    app=app,
    config="config.toml",
    header_name="Authorization"
)

@app.get("/profile")
def get_profile():
    payload = g.payload
    if payload:
        return jsonify(payload)
    else:
        return jsonify({"error": "Unauthorized"}), 401
```
