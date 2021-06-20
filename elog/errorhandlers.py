from flask import jsonify, render_template

from . import elap as app
from . import error_signal_sent, errortraps
from .helpers import InvalidAuthentication

DISPLAY = app.config.get("SHOW_ERROR_LOG")


# noinspection PyUnresolvedReferences
@app.errorhandler(400)
def error400(error):
    """Handles abort(400) calls in code."""
    result = errortraps.log_details(getattr(error, "code", None), display=DISPLAY)
    # whoosh_log.delay(result, 'ELIX')  # saves into the whoosh DB for analysis
    error_signal_sent.send(
        app, result=result, where="ELIX"
    )  # saves into the whoosh DB for analysis

    return render_template("errors/400.html"), 400


# noinspection PyUnresolvedReferences
@app.errorhandler(403)
def error403(error):
    """Handles abort(403) calls in code."""
    # print traceback.format_exc()

    result = errortraps.log_details(getattr(error, "code", None), display=DISPLAY)
    # whoosh_log.delay(result, 'ELIX')  # saves into the whoosh DB for analysis
    error_signal_sent.send(
        app, result=result, where="ELIX"
    )  # saves into the whoosh DB for analysis

    return render_template("errors/403.html"), 403


# noinspection PyUnresolvedReferences
@app.errorhandler(404)
def error404(error):
    """Handles abort(404) calls in code."""
    # print traceback.format_exc()

    result = errortraps.log_details(getattr(error, "code", None), display=DISPLAY)
    error_signal_sent.send(
        app, result=result, where="ELIX"
    )  # saves into the whoosh DB for analysis

    return render_template("errors/404.html"), 404


# noinspection PyUnresolvedReferences
@app.errorhandler(405)
def error405(error):
    """Handles abort(405) calls in code."""
    # print traceback.format_exc()

    result = errortraps.log_details(getattr(error, "code", None), display=DISPLAY)
    error_signal_sent.send(
        app, result=result, where="ELIX"
    )  # saves into the whoosh DB for analysis

    return render_template("errors/405.html"), 405


# noinspection PyUnusedLocal,PyUnresolvedReferences
@app.errorhandler(500)
def error500(error):
    """
    Handles abort(500) calls in code.
    """

    result = errortraps.log_details(500, display=DISPLAY)

    # whoosh_log.delay(result, 'ELIX')  # saves into the whoosh DB for analysis
    error_signal_sent.send(app, result=result, where="ELIX")
    return render_template("errors/500.html"), 500


@app.errorhandler(InvalidAuthentication)
def unknown_useragent(error):
    result = errortraps.log_details(413, display=DISPLAY)
    error_signal_sent.send(app, result=result, where="ELIX")
    return jsonify({"error": error.args[0]}), 413


# noinspection PyUnusedLocal,PyUnresolvedReferences
@app.errorhandler(Exception)
def unhandled_exception(error):
    result = errortraps.log_details(500, display=DISPLAY)

    # whoosh_log.delay(result, 'ELIX')  # saves into the whoosh DB for analysis
    error_signal_sent.send(app, result=result, where="ELIX")
    return render_template("errors/500.html"), 500
