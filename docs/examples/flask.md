## JWT

```python
from flask import Flask, request, jsonify
from jam import Jam


config = {
    "auth_type": "jwt",
    "secret_key": "SECRET"
}

app = Flask(__name__)
jam = Jam(config)


@app.post("/user/auth")
def auth_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    token = jam.gen_jwt_token({"username": username})
    return jsonify({"token": token})


@app.get("/user")
def get_user():
    token = request.args.get("token")
    payload = jam.verify_jwt_token(token, False, False)
    return jsonify({"username": payload["username"]})
```

## Sessions

```python
from flask import Flask, request, jsonify
from jam import Jam


config = {
    "auth_type": "session",
    "session_type": "redis",
    "is_session_crypt": False,
    "redis_uri": "redis://0.0.0.0:6379/0"
}

app = Flask(__name__)
jam = Jam(config)


@app.post("/user/auth")
def auth_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    session_id = jam.create_session(
        session_key=username,
        data={
            "username": username,
            "another": "data"
        }
    )
    return jsonify({"session_id": session_id})


@app.get("/user")
def get_user():
    session_id = request.args.get("session_id")
    data = jam.get_session(session_id)
    return jsonify({"username": data["username"]})
```
