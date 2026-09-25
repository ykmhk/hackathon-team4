from flask import Blueprint

symptom_checker = Blueprint(
    "symptom_checker",
    __name__
)

from . import views