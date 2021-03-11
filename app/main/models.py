from . import ModelMixin
from . import db

#
users_challenges = db.Table("users_challenges",
                            db.Column("user_id", db.ForeignKey('user.id'), primary_key=True),
                            db.Column("challenge_id", db.ForeignKey("challenges.id"), primary_key=True)
                            )


class Challenges(db.Model, ModelMixin):
    id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)

    challenge_text = db.Column(db.String(500), nullable=False)
    times_completed = db.Column(db.Integer(), default=0)
    checked = db.Column(db.Boolean(), default=True)



# class Notifications(db.Model, ModelMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#
#     title = db.Column(db.String(512), nullable=False)
#     date = db.Column(db.Integer(), nullable=False)
#     user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))


class Description(db.Model, ModelMixin):
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(2000), nullable=True)




