from flask import render_template, redirect, url_for, session
from flask import Blueprint
from flask_dance.contrib.google import make_google_blueprint, google
from .. import app, login_manager
from .. import db
from ..models.UserModel import User
from flask_login import login_user, logout_user
from .util import *
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError


auth_bp = Blueprint('auth', __name__)

google_bp = make_google_blueprint(client_id='826108091887-4tj9nulbl2jc879kjor41eaeoag626qt.apps.googleusercontent.com',
                                   client_secret='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',
                                   redirect_to ='auth.login',
                                   scope=["profile", "email"])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET'])
def login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    try:
        resp = google.get('/oauth2/v2/userinfo')
        assert resp.ok, resp.text
    except (InvalidGrantError, TokenExpiredError) as e:  # or maybe any OAuth2Error
        return redirect(url_for("google.login"))

    userdata = resp.json()
    user_email = userdata['email']
    user_name = userdata['name'] 

    user = User.query.filter_by(email = user_email).first()
    if not user:
        user = User(name = user_name, email = user_email)
        db.session.add(user)
        db.session.commit()

    current_user = get_current_user()
    user.merge_with_guest_user(current_user)

    logout_user()
    login_user(user)
    return redirect(url_for('shop.shop'))

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id = int(user_id)).first()
    if not user:
        return None
    return user

@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home.home'))


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(google_bp, url_prefix='/google_login')
