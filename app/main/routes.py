from datetime import date

import flask
import flask_login
import flask_mail
from flask import request, session
from sqlalchemy.sql.functions import user
import random

import app
from . import User
from . import blueprint  # variables
from . import mail_manager
from . import models, forms, db  # modules
from .forms import ChallengeCompleted
from .models import Challenges
from ..utils import send_email


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


# Challenged Deeds
@blueprint.route("/challenge/", methods=['GET', 'POST'], defaults={"id": None})
@blueprint.route("/challenge/<int:id>")
def challenge(id):
    #     # challenged = Challenges.query.all()
    #     challenged = Challenges.query.filter_by(id=session["_user_id"]).first().challenge_text
    #
    #     challenges_achieved = User.query.filter_by(id=session["_user_id"]).first().achieved_challenges
    #     deeds_times = Challenges.query.filter_by(id=session["_user_id"]).first().times_completed
    #
    #     if challenges_achieved is None:
    #         challenges_achieved = 0
    #     # session.query(User.filter_by(id = session["_user_id"])).first()
    #
    #     # print(User.query.filter_by(id=session["_user_id"]).first().achieved_challenges)
    #
    #     if request.method == 'POST':
    #         click = request.form['achieved_button']
    #         if click == 'Challenge Completed':
    #             challenges_achieved += 1
    #             deeds_times += 1
    #             # models.Challenges.filter_by(id=id).first()
    #             # update value in Database User.query.filter_by(id=session["_user_id"]).first().achieved_challenges
    #             # challenged = random.choice(challenged)
    #             flask.flash("Challenge achieved, you are amazing", category="success")
    #         return flask.render_template("challenges.html", new_challenge=challenged,
    #                                      challenges_achieved=challenges_achieved)
    #
    #     return flask.render_template("challenges.html", new_challenge=challenged, challenges_achieved=challenges_achieved)
    #
    #
    # schedule.every().day.at("00:00").do(challenge)

    # form = ChallengeCompleted(request.form)

    challenged = flask_login.current_user.last_challenge
    user_info = User.query.filter_by(id=session["_user_id"]).first()
    deeds_info = Challenges.query.filter_by(id=session["_user_id"]).first()
    # deeds_info = Challenges.query.all
    challenges_achieved = User.query.filter_by(id=session["_user_id"]).first().achieved_challenges
    deeds_times = Challenges.query.filter_by(id=session["_user_id"]).first().times_completed

    completed = flask_login.current_user.today_completed

    print(deeds_info)
    print(deeds_times)

    if challenges_achieved is None:
        challenges_achieved = 0

    if deeds_times is None:
        deeds_times = 0

    form = ChallengeCompleted(request.form)

    if request.method == "POST":
        challenges_achieved += 1
        user_info.achieved_challenges = challenges_achieved

        deeds_times += 1
        deeds_info.times_completed = deeds_times

        completed = True

        db.session.add(user_info)
        db.session.add(deeds_info)
        db.session.commit()

        flask.flash("Challenge achieved, you are amazing", category="success")

        return flask.render_template("challenges.html", new_challenge=challenged,
                                     challenges_achieved=challenges_achieved, form=form, completed=completed)

    return flask.render_template("challenges.html", new_challenge=challenged, challenges_achieved=challenges_achieved,
                                 form=form, completed=completed)



# @app.route("/notifications")
# def notifications():
#     notifications = flask_login.current_user.notifications()
#     return flask.redirect("/")

# User can submit ideas of deeds
@blueprint.route("/propdeeds/", methods=["GET", "POST"])
def propdeeds():
    form = forms.AddDeedsForm()

    print(form.description)

    title = request.form.get("title")
    description = request.form.get("description")

    if flask.request.method == "POST" and form.validate_on_submit():


        # Send it to me by mail
        send_email(
            f"{user.name} propose a new deeds",
            f"title: {title} \n description: {description}",
            "GoDeedzy@gmail.com",
        )

        print(form.description)

        flask.flash("Thank you for your support, we will review your deeds and add it on our Database",
                    category="success")
        return flask.redirect("/")

    return flask.render_template("add_deeds.html", form=form)


# Retrieve the list of deeds and number of times done
@blueprint.route("/deeds/", methods=["GET", "POST"])
def display_deeds():
    # Retrieve the list of all the deeds

    form = forms.CompletedDeedsForm()
    deeds = Challenges.query.all()
    # deeds = Challenges.query.filter_by(id=session["_user_id"]).first()
    deeds_times = Challenges.query.filter_by(id=session["_user_id"]).first().times_completed
    deeds_info = Challenges.query.filter_by(id=session["_user_id"]).first()
    checked = Challenges.checked

    print(deeds)

    if deeds_times is None:
        deeds_times = 0

    if request.method == "POST":
        request.form.getlist('mygooddeeds')

        challenge.checked = True

        deeds_times += 1
        deeds.times_completed = deeds_times

        db.session.add(deeds_times)
        db.session.commit()

        flask.flash("You are amazing")
        return flask.render_template("goodlist.html", form=form, deeds=deeds, checked=checked)

    return flask.render_template("goodlist.html", form=form, deeds=deeds, checked=checked)


@blueprint.route("/profile/")
def profile():

    deeds = Challenges.query.all()

    return flask.render_template("profile.html", deeds=deeds)
