from flask import Flask
from flask_extend_headers import ExtendHeaders


app = Flask(__name__)
app.debug = True

app.config["EXTEND_HEADERS_KEY"] = "accept-version"

extend_headers = ExtendHeaders(app)


def no_default_endpoint_v1():
    return {"version": "v1"}, 200


def no_default_endpoint_v2():
    return {"version": "v2"}, 200


@app.route("/no_default_endpoint")
@extend_headers.register(
    extensions={
        "application/v1": no_default_endpoint_v1,
        "application/v2": no_default_endpoint_v2,
    }
)
def no_default_endpoint():
    return {"version": "v0"}, 200


def default_endpoint_v2():
    return {"version": "v2"}, 200


def default_endpoint_v3():
    return {"version": "v3"}, 200


@app.route("/default_endpoint")
@extend_headers.register(
    extensions={
        "application/v2": default_endpoint_v2,
        "application/v3": default_endpoint_v3,
    },
    default="application/v1",
)
def default_endpoint_v1():
    return {"version": "v1"}, 200
