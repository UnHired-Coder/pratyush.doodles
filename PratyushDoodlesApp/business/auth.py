from flask import render_template, redirect, url_for, session
from flask import Blueprint
from flask_dance.contrib.google import make_google_blueprint, google
from .. import app, login_manager
from .. import db
from ..models.UserModel import User
from flask_login import login_user, logout_user


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
    resp = google.get('/oauth2/v2/userinfo')

    if not (resp.ok and resp.text):
        socketio.emit('error', 'Something went wrong, try again.')
        return render_template('index.html', data={})

    userdata = resp.json()
    user_email = userdata['email']
    user_name = userdata['name'] 

    user = User.query.filter_by(email = user_email).first()
    if not user:
        user = User(name = user_name, email = user_email)
        db.session.add(user)
        db.session.commit()

    data = {
        'user': user
    }

    login_user(user)
    return render_template('index.html', data=data)

@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home.home'))


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(google_bp, url_prefix='/google_login')
