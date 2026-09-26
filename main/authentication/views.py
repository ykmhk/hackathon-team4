"""HTTP routes for user authentication."""

from flask import current_app, flash, redirect, render_template, session, url_for

from main.authentication import authentication_blueprint, services
from main.authentication.decorators import login_required
from main.authentication.forms import LoginForm, RegistrationForm


@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Display the registration form and create a new account when submitted."""
    form = RegistrationForm()

    if form.validate_on_submit():
        repository = current_app.config["REPOSITORY"]

        try:
            services.register_user(
                user_name=form.username.data,
                password=form.password.data,
                repository=repository,
            )
        except ValueError as error:
            form.username.errors.append(str(error))
        else:
            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("authentication.login"))

    return render_template("authentication/register.html", form=form)


@authentication_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Display the login form and create a session for valid credentials."""
    form = LoginForm()

    if form.validate_on_submit():
        repository = current_app.config["REPOSITORY"]
        user = services.authenticate_user(
            user_name=form.username.data,
            password=form.password.data,
            repository=repository,
        )

        if user is None:
            form.password.errors.append("Invalid username or password.")
        else:
            session.clear()
            session["username"] = user.user_name

            flash("You are now logged in.", "success")
            return redirect(url_for("home.home"))

    return render_template("authentication/login.html", form=form)


@authentication_blueprint.post("/logout")
@login_required
def logout():
    """End the current user's session and return to the home page."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home.home"))
