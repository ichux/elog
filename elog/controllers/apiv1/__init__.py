from flask import Blueprint

v1_api = Blueprint("apiv1", __name__)

from elog.controllers.apiv1 import apiv1_view  # noqa: F401 E402


@v1_api.before_request
def v1_api_before_request():
    """This will occur after the application's 'before request' has been called."""
    pass


@v1_api.after_request
def v1_api_after_request(response):
    """This will occur after the application's 'after request' has been called."""
    return response
