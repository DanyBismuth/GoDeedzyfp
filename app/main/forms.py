import flask_wtf
import wtforms
from wtforms import validators as vld
import string


class AddDeedsForm(flask_wtf.FlaskForm):
    title = wtforms.StringField("Title of the deeds: ")
    description = wtforms.StringField("Description of the deeds: ")

    submit = wtforms.SubmitField("Send")


class CompletedDeedsForm(flask_wtf.FlaskForm):
    submit = wtforms.SubmitField("Confirm")


# class ChallengeCompleted(flask_wtf.FlaskForm):
#     submit = wtforms.SubmitField("Challenge Completed")
