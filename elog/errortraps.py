import json
import linecache
import secrets
import sys
import traceback
from datetime import datetime

from flask import request
from ua_parser import user_agent_parser  # type: ignore
from werkzeug.user_agent import UserAgent
from werkzeug.utils import cached_property

from .helpers import extract_vars


class ParsedUserAgent(UserAgent):
    @cached_property
    def _details(self):
        return user_agent_parser.Parse(self.string)

    @property
    def platform(self):
        return self._details["os"]["family"]

    @property
    def browser(self):
        return self._details["user_agent"]["family"]

    @property
    def version(self):
        return ".".join(
            key
            for key in ("major", "minor", "patch")
            if (key != self._details["user_agent"][key]) is not None
        )


def distinct_id(length=64):
    """
    Generate a random id to be used in tracking the error
    """

    secrets.randbits(length)
    return str(secrets.randbits(length))


def tracer(start, middle, tb, limit=None):
    if limit is None:
        if hasattr(sys, "tracebacklimit"):
            limit = sys.tracebacklimit

    error_type, error_msg = "{}".format(start), "{}".format(middle)
    n, error_traceback, terminator = 0, "", "\n"

    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        function = co.co_name
        variables = f.f_locals

        error_traceback += (
            'File "%s", line %d, in %s' % (filename, lineno, function) + terminator
        )

        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)

        if line:
            error_traceback += "  " + line.strip() + terminator
            error_traceback += f"variables: {variables}" + terminator * 2

        tb = tb.tb_next
        n += 1

    return error_type, error_msg, error_traceback


def log_details(code, display=False):
    """
    from_ = request.referrer or (request.environ.get('HTTP_REFERER') or request.headers.get("Referer"))

    In the most common cases, request.data is going to be empty, because, as stated in the docs,
    it's used as a fallback:

    request.data Contains the incoming request data as string in case it came with a mimetype Flask does not handle.

    request.args : If you want the parameters in the URL
    request.form : If you want the information in the body (as sent by a html POST form)
    request.values : If you want both
    :return: json
    """
    noticed = datetime.utcnow()
    error_time = noticed.isoformat() + "Z"
    # data = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else
    # request.form.getlist(key)[0]) for key in request.form.keys())

    data = request.form  # extract_vars(request.form)

    if "password" in extract_vars(request.form).keys():
        data = dict(data)
        data.pop(
            "password", None
        )  # removes the password if found, else remove what suites you

    error_type, error_msg, error_traceback = tracer(*sys.exc_info())

    if display:
        traceback.print_exception(*sys.exc_info())

    ua = request.headers.get("User-Agent", "")
    parsed_ua = ParsedUserAgent(ua)
    return {
        "id": distinct_id(),
        "ip": str(get_real_ip()),
        "requestpath": request.path,
        "httpmethod": str(request.method),
        "useragent": ua,
        "userplatform": parsed_ua.platform,
        "userbrowser": parsed_ua.browser,
        "userbrowserversion": parsed_ua.version,
        "referrer": str(request.referrer),
        # json.dumps(request.args, indent=1, sort_keys=True)
        "requestargs": json.dumps(request.args),  # request.args.to_dict()
        "postvalues": json.dumps(data),  # json.dumps(data, indent=1, sort_keys=True)
        "errortype": str(error_type),
        "errormsg": str(error_msg.encode("utf-8")),
        "when": str(error_time),
        "errortraceback": str(error_traceback),
        "code": code,  # This is a NUMERIC field in Whoosh
        "date": noticed,  # this line is essential to be able to make the query "date:today" work!
    }


def get_real_ip():
    # use all known hack to get the real ip address of the visitor who caused the error
    address = request.headers.get("X-Forwarded-For")
    if address is not None:
        # An 'X-Forwarded-For' header includes a comma separated list of the
        # addresses, the first address being the actual remote address.
        ip = address.encode("utf-8").split(b",")[0].strip()
    else:
        # this is the original way of getting the IP in this application
        ip = request.environ.get(
            "HTTP_X_REAL_IP", request.remote_addr
        )  # This is important for nginx config
    return ip
