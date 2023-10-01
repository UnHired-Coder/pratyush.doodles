from flask import render_template
from flask import Blueprint
from .. import app

others_bp = Blueprint('others', __name__)
# Define routes and views for the 'auth' Blueprint
@others_bp.route('/questions')
def questions():
    return render_template('questions.html')


@others_bp.route('/contact')
def contact():
    return render_template('contact.html')


@others_bp.route('/about')
def about():
    return render_template('about.html')

app.register_blueprint(others_bp)