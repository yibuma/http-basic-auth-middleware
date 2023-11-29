import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from http_basic_auth import HTTPBasicAuthMiddleware

app = FastAPI()
HTTPBasicAuthMiddleware.setup(
    app=app,
    check_handler=lambda cred: cred.username == "user" and cred.password == "password",
    ignore_paths=["/ignore"],
    scheme_name="s2sbc",
    realm="s2sbcr",
)
app.get("/ignore")(lambda: {"status": "ok"})
app.get("/test")(lambda: {"status": "ok"})
app.get("/")(lambda: {"status": "ok"})
client = TestClient(app)


class TestHTTPBasicAuth(unittest.TestCase):
    def test_unauth(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    def test_incorrect(self):
        response = client.get("/", auth=("user", "incorrect"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Incorrect credentials"})

    def test_correct(self):
        response = client.get("/", auth=("user", "password"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ignore(self):
        response = client.get("/ignore")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ignore_auth_correct(self):
        response = client.get("/ignore", auth=("user", "password"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ignore_auth_incorrect(self):
        response = client.get("/ignore", auth=("user", "incorrect"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
