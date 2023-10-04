from flask import session
from ..models.UserModel import User

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.filter_by(id = user_id).first()
    return None    
