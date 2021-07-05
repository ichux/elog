from datetime import datetime

from flask import jsonify, request

from elog import csrf
from elog import elap as app
from elog import error_signal_sent
from elog.controllers.apiv1 import v1_api
from elog.errortraps import distinct_id
from elog.helpers import InvalidAuthentication
from elog.models.profile import UserAccess


@v1_api.route("/elog", methods=["POST"])
@csrf.exempt
def error_log():
    external_app_id = request.headers.get("EXTERNAL-APP-ID")
    flag = False

    # result = extract_vars(request.form)
    # print('gotten: {}'.format(result))

    ip = request.json.get("ip")

    confirm_ip = UserAccess.query.filter_by(ip_address=ip).all()
    if confirm_ip is None:
        raise InvalidAuthentication(f"Unknown IP address: {ip}")

    for each in confirm_ip:
        if each.external_app_id == external_app_id:
            flag = True
            break

    if not flag:
        raise InvalidAuthentication(f"Unknown External APP ID: {external_app_id}")

    result = {
        "id": distinct_id(),
        "ip": request.json.get("ip"),
        "requestpath": request.json.get("requestpath"),
        "httpmethod": request.json.get("httpmethod"),
        "useragent": request.json.get("useragent"),
        "userplatform": request.json.get("userplatform"),
        "userbrowser": request.json.get("userbrowser"),
        "userbrowserversion": request.json.get("userbrowserversion"),
        "referrer": request.json.get("referrer"),
        "requestargs": request.json.get("requestargs"),
        "postvalues": request.json.get("postvalues"),
        "errortype": request.json.get("errortype"),
        "errormsg": request.json.get("errormsg"),
        "when": request.json.get("when"),
        "errortraceback": request.json.get("errortraceback"),
        # This is a NUMERIC field in Whoosh and without converting it to an int, it threw an error
        "code": int(request.json.get("code")),
        # this line is essential to be able to make the query "date:today" work!
        # it has to be converted back to the 'datetime.datetime' format
        "date": datetime.strptime(request.json.get("date"), "%Y-%m-%dT%H:%M:%S"),
    }

    error_signal_sent.send(app, result=result, where="ELIX")
    return jsonify({"success": True})
