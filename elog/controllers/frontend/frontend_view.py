from flask import jsonify, render_template, request
from flask_login import login_required  # type: ignore

from elog import data_tables_display, remove_by_id
from elog.controllers.frontend import frontend
from elog.helpers import prepare_arguments


# noinspection PyUnresolvedReferences
@frontend.route("/")
@login_required
def index():
    # print(session['user_id'], session['_id'])
    return render_template("elog.html")


@frontend.route("/data", methods=["GET"])
@login_required
def data():
    request_args = prepare_arguments(request.args)

    print(request_args.get("search[value]"))
    qs = request_args.get("search[value]") or "date:today"

    # this is a hack that ensure 1 comes in instead of the default
    # zero that datatables might send in
    start = request_args.get("start") or 1

    # Datatable sends in -1 when 'All' is chosen from the interface, so,
    # a maximum of 200 results are pulled out from the Whoosh
    length = 200 if request_args.get("length", -1) < 0 else request_args.get("length")

    result = data_tables_display(qs, start, length, "ELIX")

    draw = request_args.get("draw")
    if draw:
        result.update({"draw": request_args.get("draw")})

    return jsonify(result)


@frontend.route("/elog-delete", methods=["POST"])
@login_required
def elog_delete():
    returned = request.get_json()
    if returned:
        listed_ids = returned.get("ids")
        if listed_ids:
            for each_id in listed_ids:
                remove_by_id(each_id)
        return jsonify({"success": True})
    return jsonify({})
