from flask import session
from ..models.UserModel import User
from flask_login import  current_user, login_user
from .. import db
import time


def get_current_user():
    if  current_user.is_anonymous:
        ts = time.time()

        user = User(name = "guest_"+str(ts), email = "guest_"+str(ts), guest_user = True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user
    return current_user

