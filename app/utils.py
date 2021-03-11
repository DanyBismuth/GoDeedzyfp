import flask
import flask_sqlalchemy
import flask_migrate
import flask_login
import flask_mail
import os

import config
from app import db, mail_manager


# from app import mail_manager


def send_email(subject, body, recipients):
    msg = flask_mail.Message(
        subject=subject,
        body=body,
        recipients=recipients.split(),
        sender=flask.current_app.config["MAIL_USERNAME"],
    )
    print(flask.current_app.config["MAIL_USERNAME"])
    mail_manager.send(msg)

def send_mail(subject, body, recipients):
    msg = flask_mail.Message(
        subject=subject,
        body=body,
        recipients=recipients,
        sender=flask.current_app.config["MAIL_USERNAME"],
    )

    print(flask.current_app.config["MAIL_USERNAME"])
    mail_manager.send(msg)


class ModelMixin():

    id = db.Column(db.Integer(), primary_key=True)

    def save(self):
        # Add it to the database
        db.session.add(self)

        # Commit the changes
        try:
            db.session.commit()
            return True
        except:
            # Something went wrong --> rollback
            db.session.rollback()
            return False

class FormUtils():

    def quick_html(self):

        return """
            <form method="POST">
                {{ form.hidden_tag() }}
                <p>
                    {{ form.username.label }}
                    {{ form.username() }}
                </p>
                <p>
                    {{ form.password.label }}
                    {{ form.password() }}
                </p>

                {{ form.submit() }}
            </form>
        """
