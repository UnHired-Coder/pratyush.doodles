from flask import render_template
from flask import Blueprint
from .. import app
from .util import *


others_bp = Blueprint('others', __name__)
# Define routes and views for the 'auth' Blueprint
@others_bp.route('/questions')
def questions():
    data = {
        'user': get_current_user()
    }
    return render_template('questions.html', data=data)

@others_bp.route('/contact')
def contact():
    data = {
        'user': get_current_user()
    }
    return render_template('contact.html', data=data)


@others_bp.route('/about')
def about():
    data = {
        'user': get_current_user()
    }
    return render_template('about.html', data=data)

app.register_blueprint(others_bp)