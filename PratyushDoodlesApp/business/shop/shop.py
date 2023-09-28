from flask import render_template
from flask import Blueprint
from ... import app


shop_bp = Blueprint('shop', __name__)

# Define routes and views for the 'auth' Blueprint
@shop_bp.route('/shop')
def shop():
    return render_template('shop.html')

app.register_blueprint(shop_bp)