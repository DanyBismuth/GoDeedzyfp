import flask_login
import werkzeug

from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import AdminIndexView
from flask import redirect,request,url_for


from . import db
from . import ModelMixin

class User(db.Model, flask_login.UserMixin, ModelMixin):

    id = db.Column(db.Integer(), primary_key=True)

    name     = db.Column(db.String(64), nullable=False, unique=True)
    email     = db.Column(db.String(512))

    password = db.Column(db.String(512), nullable=False)
    #
    # notifications = db.relationship("Notifications", backref="user")
    # daily_challenge = db.Column(db.DateTime(), nullable=True)
    achieved_challenges = db.Column(db.Integer(), default = 0)


    def __repr__(self):
        return '<Name %r>' % self.name

    def set_password(self, new):
        """
        Set a new password for this user
        """

        pwd_hash = generate_password_hash(new)

        self.password = pwd_hash


    def check_password(self, pwd):
        """
        Check the given password against this user's password
        """

        return check_password_hash(self.password, pwd)