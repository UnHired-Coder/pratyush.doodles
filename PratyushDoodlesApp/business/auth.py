from flask import render_template, redirect, url_for, session
from flask import Blueprint
from flask_dance.contrib.google import make_google_blueprint, google
from .. import app
from .. import db
from ..models.UserModel import User


auth_bp = Blueprint('auth', __name__)

google_bp = make_google_blueprint(client_id='826108091887-4tj9nulbl2jc879kjor41eaeoag626qt.apps.googleusercontent.com',
                                   client_secret='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',
                                   redirect_to ='auth.login',
                                   scope=["profile", "email"])

@auth_bp.route('/login')
def login():
    print("login")
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text

    user = add_user(resp.json())
    data = {
        'user': user
    }

    return render_template('index.html', data=data)

def add_user(userdata):
    user_name = userdata['name']  
    user_email = userdata['email']

    user = User(name = user_name, email = user_email)
    db.session.add(user)
    db.session.commit()
    session['user'] = userdata

    return user

@auth_bp.route('/logout')
def logout():
    session.pop('user')
    
    return redirect(url_for('home.home'))
    


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(google_bp, url_prefix='/google_login')
