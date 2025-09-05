from FlaskMIS import db, login_manager
from flask import session
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user_role = session.get("user_role")  # Store role in session at login
    if user_role == "student":
        return Students.query.get(int(user_id))
    return Admins.query.get(int(user_id))

class Admins(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}')"
class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = True, nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}')"