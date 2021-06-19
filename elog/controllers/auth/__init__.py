from flask import Blueprint

auth = Blueprint("auth", __name__)

from elog.controllers.auth import auth_view  # noqa: F401 E402


@auth.before_request
def auth_before_request():
    """This will occur after the app's 'before request' has been called.."""
    pass
