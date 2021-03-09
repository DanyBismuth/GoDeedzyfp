import flask_wtf
import wtforms
from wtforms import validators as vld
import string



### VALIDATORS

def validate_username(form, field):
    """
    Validate the username, rules:
        - It needs to have more than 6 characters
        - No weird symbols (Only letters and numbers)
        - No more than 12 characters
    """

    if len(field.data) < 6:
        raise vld.ValidationError("Username has to be at least 6 characters")

    for symbol in string.punctuation:
        if symbol in field.data:
            raise vld.ValidationError("No symbols allowed in username")

    if len(field.data) >= 12:
        raise vld.ValidationError("Maximum characters allowed is 12")

def validate_password(form, field):
    """
    Validate the password, rules:
        - At least one uppercased letter, one lowercased letter and one symbol
        - At least 8 characters
        - No more than 12 characters
        - Not something from this list: ["chocolate", "password", "p4ssw0rd!"]
    """
    password = field.data

    # Forbidden passwords
    black_list = [
        "password",
    ]

    # Check if there is at least one uppercased letter
    if password == password.lower():
        raise vld.ValidationError("Password need to contain at least one uppercased letter")

    # Check if there is at least one lowercased letter
    if password == password.upper():
        raise vld.ValidationError("Password need to contain at least one lowercased letter")

    if not 8 <= len(password) <= 12:
        raise vld.ValidationError("Password length need to be between 8 and 12")

    if password in blacklist:
        raise vld.ValidationError("This password is too famous")

# CLASSES

class SigninForm(flask_wtf.FlaskForm):

    username = wtforms.StringField("Username: ")
    password = wtforms.PasswordField("Password: ")

    submit  = wtforms.SubmitField("Sign in")

class SignupForm(flask_wtf.FlaskForm):

    username = wtforms.StringField("Username: ", validators=[vld.DataRequired(), validate_username])
    email = wtforms.StringField("Email: ", validators=[vld.Email()])
    password = wtforms.PasswordField("Password: ", validators=[vld.DataRequired()])

    submit  = wtforms.SubmitField("Sign up")

class ResetPasswordForm(flask_wtf.FlaskForm):

    email    = wtforms.StringField("Email: ", validators=[vld.Email()])

    submit  = wtforms.SubmitField("Submit button")