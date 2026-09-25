"""Generic placeholder blueprint for a starter project."""

from flask import Blueprint, render_template

items_blueprint = Blueprint("items", __name__)


@items_blueprint.route("/browse")
def browse():
    return render_template("index.html")


@items_blueprint.route("/search")
def search():
    return render_template("index.html")
