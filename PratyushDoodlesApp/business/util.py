from flask import session
from ..models.UserModel import User

def get_current_user():
    userdata = session.get('user')
    user = None  
    if userdata:
        user = User(name=userdata['name'], email=userdata['email'])
    return user    
