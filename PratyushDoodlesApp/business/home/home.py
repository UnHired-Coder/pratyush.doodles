from flask import render_template
from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home():
    return render_template('index.html')