"""Flask-WTF forms and validation rules for authentication."""

from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class PasswordValid:
    """Validate the password policy required for new registrations."""

    def __init__(self, message=None):
        self.message = message or (
            "Password must be at least 8 characters and include an uppercase "
            "letter, a lowercase letter, and a digit."
        )

    def __call__(self, form, field):
        """Raise a validation error when the password does not meet the policy."""
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()

        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    """Collect and validate details for a new Music Library account."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, message="Username must be at least 3 characters long."),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            PasswordValid(),
        ],
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Collect login credentials without applying registration-only rules."""

    username = StringField(
        "Username",
        validators=[DataRequired(message="Username is required.")],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
    )

    submit = SubmitField("Log in")