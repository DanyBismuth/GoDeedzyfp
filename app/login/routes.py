import random

import flask
import flask_login
import jwt

from . import db
from . import blueprint
from . import forms, models
from . import send_mail

@blueprint.route("/sign-up/", methods=["GET", "POST"])
def add_user():

    form = forms.SignupForm()

    # Catch the POST request and do something with it
    if flask.request.method == "POST":
        # print(models.User.query.all())
        # Check if the form is valid
        if form.validate_on_submit():

            # Create a user
            # Need to use keyword arguments (arg=value, arg2=value2...)
            new_user = models.User(
                name=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )

            new_user.set_password(form.password.data)
            print("test")
            # Save it
            if new_user.save():
                flask.flash(f"User {new_user.name} created successfully", category="success")
            else:
                flask.flash("Something went wrong..")

            return flask.redirect("/")

    return flask.render_template("signup.html", form=form)

@blueprint.route("/sign-in/", methods=["GET", "POST"])
def signin():

    form = forms.SigninForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():

            # Check credentials
            user = models.User.query.filter_by(name=form.username.data).first()

            if user.check_password(form.password.data):
                # if it matches, log him in (Use flask_login.login_user(<user_obj>) to log someone in)
                flask_login.login_user(user)

                flask.flash(f"Welcome, {user.name}")
                return flask.redirect("/")
            else:
                flask.flash("Wrong credentials")

    return flask.render_template("signin.html", form=form)


@blueprint.route("/sign-out/")
def signout():
    flask_login.logout_user()
    return flask.redirect("/")

@blueprint.route("/reset_password/", methods=["GET", "POST"])
def reset_password():

    form = forms.ResetPasswordForm()

    if flask.request.method == "POST":

        if form.validate_on_submit():

            # Retrieve the user object
            user = models.User.query.filter_by(email=form.email.data).first()

            if user is not None:
                # Generate random password
                pwd_len = random.randint(8, 12)
                pwd = ""
                # Add one uppercased letter
                pwd += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

                # Add one lowercased letter
                pwd += random.choice("abcdefghijklmnopqrstuvwxyz")

                # Add one symbol
                pwd += random.choice("!@#$%^&*()_+''")

                # Fill the missing letters
                for i in range(pwd_len-3):
                    pwd += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+''")


                # Create a JSON message that contains his new password
                payload = {
                    "user_id": user.id,
                    "new_pwd": pwd,
                }

                encoded = jwt.encode(
                    payload,
                    flask.current_app.config["SECRET_KEY"],
                    algorithm="HS256",
                )

                link = flask.url_for("login_blueprint.reset_password_after", payload=encoded, _external=True)

                # Send it to the user by mail
                send_mail(
                    subject="Password reset",
                    body=f"Hey {user.name} ! Follow this link to reset your password: {link}",
                    recipients=[user.email]
                )

                return flask.redirect("/")
            else:
                flask.flash("The mail address doesn't exist")


    return flask.render_template("reset_password.html", form=form)

@blueprint.route("/reset-password/<payload>")
def reset_password_after(payload):


    decoded = jwt.decode(
        payload,
        flask.current_app.config["SECRET_KEY"],
        algorithms=["HS256"],
    )
    user_id = decoded["user_id"]
    new_pwd = decoded["new_pwd"]

    user = models.User.query.get(user_id)
    user.set_password(new_pwd)

    flask.flash("Password reset successfully")

    return flask.redirect('/')