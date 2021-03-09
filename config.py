import os

# Name of the directory containing __init__.py
basedir = os.path.abspath("app")  # __file__ is "__init__.py"

class Config:

    SECRET_KEY = "edwoijfwoqijer"

    SQLALCHEMY_DATABASE_URI = "postgres://postgres:@Banana0907@localhost:5432/godee"

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "GoDeedzy@gmail.com"
    MAIL_PASSWORD = "@Banana0907"