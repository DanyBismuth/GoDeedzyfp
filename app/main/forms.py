import flask_wtf
import wtforms
from wtforms import Form, IntegerField
import string


class AddDeedsForm(flask_wtf.FlaskForm):
    title = wtforms.StringField("Title of the deeds: ")
    description = wtforms.StringField("Description of the deeds: ")

    submit = wtforms.SubmitField("Send")


class CompletedDeedsForm(flask_wtf.FlaskForm):
    submit = wtforms.SubmitField("Confirm")


class ChallengeCompleted(Form):
    submit = IntegerField("Challenge Completed")
