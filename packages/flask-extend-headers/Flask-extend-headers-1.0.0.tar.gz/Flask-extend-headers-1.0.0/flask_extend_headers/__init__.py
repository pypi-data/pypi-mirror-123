import functools

from flask import request, current_app
from werkzeug.exceptions import NotAcceptable


class ExtendHeaders(object):
    def __init__(self, app=None, header: str = ""):
        self.app = app
        self.header = header
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("EXTEND_HEADERS_KEY", "Accept")

    @classmethod
    def register(cls, extensions: dict, default: str = ""):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                custom_header_key = current_app.config["EXTEND_HEADERS_KEY"].title()
                request_header_keys = [key for key in request.headers.keys()]
                if (
                    default
                    and custom_header_key in request_header_keys
                    and request.headers[custom_header_key] == default
                ):
                    return func(*args, **kwargs)
                elif custom_header_key in request_header_keys:
                    for extension in extensions.keys():
                        if extension == request.headers[custom_header_key]:
                            return extensions[extension](*args, **kwargs)
                elif not default:
                    return func(*args, **kwargs)
                description = f"{NotAcceptable.description} Supported entities are: {custom_header_key}"
                raise NotAcceptable(description)

            return wrapper

        return decorator
