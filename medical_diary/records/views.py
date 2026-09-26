from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash

import medical_diary.records.services as services
from medical_diary.adapters.repository import repo_instance

records_blueprint = Blueprint("records_bp", __name__, url_prefix="/records")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("authentication_bp.login"))
        return view(*args, **kwargs)
    return wrapped


@records_blueprint.route("", methods=["GET"])
@login_required
def records():
    username = session["username"]
    all_records = services.get_records_for_user(username, repo_instance)
    selected_id = request.args.get("selected")
    selected = None
    if selected_id:
        selected = services.get_record(selected_id, username, repo_instance)
    if selected is None and all_records:
        selected = all_records[0]

    return render_template(
        "records/records.html",
        records=all_records,
        selected=selected,
        records_json=[r.to_dict() for r in all_records],
    )


@records_blueprint.route("/add", methods=["POST"])
@login_required
def add_record():
    username = session["username"]
    date = request.form.get("date", "").strip()
    diagnosis = request.form.get("diagnosis", "").strip()
    prescription = request.form.get("prescription", "").strip()
    doctor_comments = request.form.get("doctor_comments", "").strip()

    try:
        record = services.add_record(username, date, diagnosis, prescription,
                                      doctor_comments, repo_instance)
        return redirect(url_for("records_bp.records", selected=record.id))
    except services.InvalidRecordException as e:
        flash(str(e))
        return redirect(url_for("records_bp.records"))


@records_blueprint.route("/search", methods=["GET"])
@login_required
def search():
    """JSON endpoint used for live search filtering in the sidebar."""
    username = session["username"]
    keyword = request.args.get("q", "")
    matches = services.search_records(username, keyword, repo_instance)
    return jsonify([r.to_dict() for r in matches])
