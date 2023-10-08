from flask import render_template
from flask import Blueprint
from .. import app
from ..models.FaqModel import Faq
from .util import *


others_bp = Blueprint('others', __name__)
# Define routes and views for the 'auth' Blueprint
@others_bp.route('/questions')
def questions():
    user = get_current_user()
    data = {
            'user': user
    }
  
    return render_template('questions.html', data=data)

@others_bp.route('/getFaqs')
def getFaqs():
    # Fetch cart items as a list of objects
    faqs = Faq.query.all()
    data = {
        'faqs' : faqs
    }

    # Render the Jinja2 template with the cart items
    rendered_template = render_template('ui/faq_item.html', data=data)
    return rendered_template


@others_bp.route('/contact')
def contact():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('contact.html', data=data)

@others_bp.route('/about')
def about():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('about.html', data=data)

app.register_blueprint(others_bp)