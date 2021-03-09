import random

import flask
import flask_mail
import schedule
from flask import request, session
from flask import flash
from sqlalchemy.sql.functions import user

import app
from . import User
from . import blueprint  # variables
from . import mail_manager
from . import models, forms  # modules
from .models import Challenges
from ..utils import send_mail


@blueprint.route("/")
def home():
    # Retrieve products

    return flask.render_template("home.html")


# How to retrieve users
@blueprint.route("/users")
def display_users():
    # Retrieve the list of all the users
    users = User.query.all()

    return flask.render_template("users_list.html", users=users)


@blueprint.route("/test-mail")
def mail_test():
    msg = flask_mail.Message(
        subject="This is a test",
        body="Hey, this mail is a test",
        recipients=["godeedzy@gmail.com"],
        sender="godeedzy@gmail.com",
    )

    mail_manager.send(msg)

    return flask.redirect("/")


# ???
@blueprint.route("/challenge/", defaults={"id": None})
@blueprint.route("/challenge/<int:id>")
def challenge(id):


    # challenged = Challenges.query.all()
    challenged = Challenges.query.filter_by(id=session["_user_id"]).first().challenge_text

    challenges_achieved = User.query.filter_by(id=session["_user_id"]).first().achieved_challenges
    deeds_times = Challenges.query.filter_by(id=session["_user_id"]).first().times_completed

    if challenges_achieved is None:
        challenges_achieved = 0
    # session.query(User.filter_by(id = session["_user_id"])).first()

    # print(User.query.filter_by(id=session["_user_id"]).first().achieved_challenges)

    if request.method == 'POST':
        if request.form['achieved_button'] == 'done':
            challenges_achieved += 1
            deeds_times += 1
            models.Challenges.filter_by(id=id).first()
            # update value in Database User.query.filter_by(id=session["_user_id"]).first().achieved_challenges
            challenged = random.choice(challenged)
            flask.flash("Challenge achieved, you are amazing", category="success")
        return flask.render_template("challenges.html", new_challenge=challenged,
                                     challenges_achieved=challenges_achieved)

    return flask.render_template("challenges.html", new_challenge=challenged, challenges_achieved=challenges_achieved)


schedule.every().day.at("00:00").do(challenge)


# form = forms.ChallengeCompleted
#
# challenged = Challenges.query.filter_by(id=session["_user_id"]).first().challenge_text
#
# challenges_achieved = User.query.filter_by(id=session["_user_id"]).first().achieved_challenges
# deeds_times = Challenges.query.filter_by(id=session["_user_id"]).first().times_completed
#
# if challenges_achieved is None:
#     challenges_achieved = 0
#
# if flask.request.method == "POST":
#     if form.validate_on_submit():
#         challenges_achieved += 1
#         deeds_times += 1
#         models.Challenges.filter_by(id=id).first()
#         challenged = random.choice(challenged)
#         flask.flash("Challenge achieved, you are amazing", category="success")
#     else:
#         flask.flash("Something went wrong..")
#     return flask.render_template("/", new_challenge=challenged)
#
# return flask.render_template("challenges.html", new_challenge=challenged,
#                              form=form)


# @app.route("/notifications")
# def notifications():
#     notifications = flask_login.current_user.notifications()
#     return flask.redirect("/")

# ???
@blueprint.route("/propdeeds/", methods=["GET", "POST"])
def propdeeds():
    form = forms.AddDeedsForm()

    if flask.request.method == "POST" and form.validate_on_submit():
        description = app.main.models.Description.query.filter_by(description=form.description.data).first()

        # Send it to me by mail
        send_mail(
            subject=f"{user.name} propose a new deeds",
            body=f"{description.description}",
            recipients="GoDeedzy@gmail.com",
        )

        flask.flash("Thank you for your support, we will review your deeds and add it on our Database", category="success")
        return flask.redirect("/")

    return flask.render_template("add_deeds.html", form=form)


# ???
@blueprint.route("/deeds/", methods=["GET", "POST"])
def display_deeds():
    # Retrieve the list of all the deeds
    form = forms.CompletedDeedsForm()
    deeds = Challenges.query.all()
    # deeds = Challenges.query.filter_by(id=session["_user_id"]).first()
    deeds_times = Challenges.query.filter_by(id=session["_user_id"]).first().times_completed

    if deeds_times is None:
        deeds_times = 0

    if request.method == "POST":
        request.form.getlist('mygooddeeds')
        deeds_times += 1

        return flask.flash("You are amazing")

    return flask.render_template("goodlist.html", form=form, deeds=deeds)


@blueprint.route("/profile/")
def profile():
    deeds = Challenges.query.all()

    return flask.render_template("profile.html", deeds=deeds)
