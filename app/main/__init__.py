import flask

from app.login import models
from app import db, login_manager, mail_manager
from app.login.models import User
blueprint = flask.Blueprint("main_blueprint", __name__)



from app.utils import ModelMixin
from . import routes, models