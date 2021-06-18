from flask import Blueprint, g
from flask_login import current_user

frontend = Blueprint("frontend", __name__)

from elog.controllers.frontend import frontend_view


@frontend.before_request
def frontend_before_request():
    """This will occur after the app's 'before request' has been called.."""
    g.user = current_user


"""
@frontend.after_request
def frontend_after_request(rv):
    headers = getattr(g, 'headers', {})
    rv.headers.extend(headers)
    return rv
"""
