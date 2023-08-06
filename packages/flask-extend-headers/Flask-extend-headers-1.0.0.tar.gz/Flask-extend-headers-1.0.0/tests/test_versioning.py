import json


import pytest


from flask_app_for_testing import app


def test_no_default():
    with app.test_client() as client:
        req = client.get("/no_default_endpoint")
        assert req.status_code == 200
        assert "v0" == json.loads(req.data.decode())["version"]


@pytest.mark.parametrize(
    "headers,status_code,version",
    [
        ("application/v1", 200, "v1"),
        ("application/v2", 200, "v2"),
    ],
)
def test_no_default_versioning(headers, status_code, version):
    with app.test_client() as client:
        req = client.get("/no_default_endpoint", headers={"accept-version": headers})
        assert req.status_code == status_code
        assert version == json.loads(req.data.decode())["version"]


@pytest.mark.parametrize(
    "headers,status_code",
    [
        ("application/v3", 406),
        ("", 406),
    ],
)
def test_no_default_not_acceptable(headers, status_code):
    with app.test_client() as client:
        req = client.get("/no_default_endpoint", headers={"accept-version": headers})
        assert req.status_code == status_code


@pytest.mark.parametrize(
    "headers,status_code,version",
    [
        ("application/v1", 200, "v1"),
        ("application/v2", 200, "v2"),
        ("application/v3", 200, "v3"),
    ],
)
def test_default_versioning(headers, status_code, version):
    with app.test_client() as client:
        req = client.get("/default_endpoint", headers={"accept-version": headers})
        assert req.status_code == status_code
        assert version == json.loads(req.data.decode())["version"]


@pytest.mark.parametrize(
    "headers,status_code",
    [
        ("application/v4", 406),
        ("", 406),
    ],
)
def test_default_not_acceptable(headers, status_code):
    with app.test_client() as client:
        req = client.get("/default_endpoint", headers={"accept-version": headers})
        assert req.status_code == status_code
