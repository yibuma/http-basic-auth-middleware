# http-basic-auth-middleware
FastAPI HTTP Basic Auth Middleware

By default, http basic auth authentication is added to all endpoints. If you only need to add http basic auth authentication to certain endpoints, you can use [FastAPI's built-in HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/).

## Installation
```bash
pip install http-basic-auth-middleware
```
or 
```bash
poetry add http-basic-auth-middleware
```

## Usage
```python
from fastapi import FastAPI
from http_basic_auth import HTTPBasicAuthMiddleware

app = FastAPI()
HTTPBasicAuthMiddleware.setup(
    app,
    check_handler=lambda cred: cred.username == "Admin" and cred.password == "password",
    ignore_paths=["/healthz", "/metrics"],  // the path that you don't want to add http basic auth
)