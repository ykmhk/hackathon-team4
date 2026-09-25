from flask import render_template

from main.home import home_blueprint


@home_blueprint.route('/')
def home():
    return render_template('index.html')