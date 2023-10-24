from flask import session
from ..models.UserModel import User
from flask_login import  current_user

def get_current_user():
    if  current_user.is_anonymous:
        return None
    return current_user

