from flask import render_template, redirect, url_for
from flask import Blueprint
from flask_dance.contrib.google import make_google_blueprint, google
from ... import app


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

    data = {
        'title': "Logged in as " +str(resp.json()['name'])
    }

    return render_template('cart.html', data=data)


@auth_bp.route('/google')
def googlelogin():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text

    data = {
        'title': "Logged in as " +str(resp.json()['name'])
    }
        
    return render_template('cart.html', data=data)

@auth_bp.route('/google/authorized')
def authorized():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text

    data = {
        'title': "Logged in as " +str(resp.json()['name'])
    }
        
    return render_template('cart.html', data=data)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(google_bp, url_prefix='/google_login')
