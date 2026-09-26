"""Flask-WTF form for submitting a track review."""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ReviewForm(FlaskForm):
    """Collect one 0-5 rating and a short written review."""

    rating = SelectField(
        "Rating",
        choices=[(score, f"{score} / 5") for score in range(6)],
        coerce=int,
        validators=[
            InputRequired(message="Please select a rating."),
            NumberRange(min=0, max=5, message="Rating must be between 0 and 5."),
        ],
    )

    review_text = TextAreaField(
        "Your review",
        validators=[
            DataRequired(message="Please write a review."),
            Length(max=500, message="Reviews must be 500 characters or fewer."),
        ],
    )

    submit = SubmitField("Post review")
