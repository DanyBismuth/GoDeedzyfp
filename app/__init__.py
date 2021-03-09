import flask
import flask_sqlalchemy
import flask_migrate
import flask_login
import flask_mail
import os

import config


# Create the virtual database
basedir = os.path.abspath(os.path.dirname(__file__))  # __file__ is "__init__.py"

# We can create managers without "app" being defined
db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
login_manager = flask_login.LoginManager()
mail_manager = flask_mail.Mail()

@login_manager.user_loader
def load_user(user_id):
    return login.models.User.query.get(user_id)

def create_app():

    from .login import blueprint as login_bp
    from app.main import blueprint as main_bp

    # Create the app controller
    app = flask.Flask(__name__)

    # for f in filters:
    #     app.jinja_env.filters[f.__name__] = f

    app.register_blueprint(login_bp)
    app.register_blueprint(main_bp)

    # Load the config directly from a class
    app.config.from_object(config.Config)

    # Initialize the app after everything has been read by python
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail_manager.init_app(app)

    @app.shell_context_processor
    def shell_predefined_variables():
        from .main import models
        from .login.models import User

        return {
            "basedir": basedir,
            "db": db,
            "models":models,
            "User": User,
            "config": config.Config,
        }

    return app


