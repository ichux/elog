from datetime import datetime

from flask import jsonify, request

from elog import csrf
from elog import elap as app
from elog import error_signal_sent
from elog.controllers.apiv1 import v1_api
from elog.errortraps import distinct_id
from elog.helpers import InvalidAuthentication
from elog.models.profile import User


@v1_api.route("/elog", methods=["POST"])
@csrf.exempt
def error_log():
    external_app_id = request.headers.get("EXTERNAL-APP-ID")

    # result = extract_vars(request.form)
    # print('gotten: {}'.format(result))

    ip = request.form.get("ip")

    confirm_ip = User.query.filter_by(ip_address=ip).first()
    if confirm_ip is None:
        raise InvalidAuthentication("Unknown IP address: {}".format(ip))

    if not (external_app_id == confirm_ip.external_app_id):
        raise InvalidAuthentication(
            "Unknown External APP ID: {}".format(external_app_id)
        )

    result = {
        "id": distinct_id(),
        "ip": request.form.get("ip"),
        "requestpath": request.form.get("requestpath"),
        "httpmethod": request.form.get("httpmethod"),
        "useragent": request.form.get("useragent"),
        "userplatform": request.form.get("userplatform"),
        "userbrowser": request.form.get("userbrowser"),
        "userbrowserversion": request.form.get("userbrowserversion"),
        "referrer": request.form.get("referrer"),
        "requestargs": request.form.get("requestargs"),
        "postvalues": request.form.get("postvalues"),
        "errortype": request.form.get("errortype"),
        "errormsg": request.form.get("errormsg"),
        "when": request.form.get("when"),
        "errortraceback": request.form.get("errortraceback"),
        # This is a NUMERIC field in Whoosh and without converting it to an int, it threw an error
        "code": int(request.form.get("code")),
        # this line is essential to be able to make the query "date:today" work!
        # it has to be converted back to the 'datetime.datetime' format
        "date": datetime.strptime(request.form.get("date"), "%Y-%m-%d %H:%M:%S.%f"),
    }

    error_signal_sent.send(app, result=result, where="ELIX")
    return jsonify({"success": True})
