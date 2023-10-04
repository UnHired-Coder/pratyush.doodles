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
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text

    userdata = resp.json()
    user_email = userdata['email']
    user_name = userdata['name'] 
    
    user = User.query.filter_by(email = user_email).first()

    if not User:
        user = User(name = user_name, email = user_email)

    data = {
        'user': user
    }

    return render_template('index.html', data=data)

@auth_bp.route('/logout')
def logout():
    session.pop('user')    
    return redirect(url_for('home.home'))


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(google_bp, url_prefix='/google_login')
