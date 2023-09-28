from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    app.secret_key = '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'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    from PratyushDoodlesApp.business.auth.auth import auth_bp
    from PratyushDoodlesApp.business.cart.cart import cart_bp
    from PratyushDoodlesApp.business.shop.shop import shop_bp
    from PratyushDoodlesApp.business.payments.payments import payments_bp
    from PratyushDoodlesApp.business.others.others import others_bp
    from PratyushDoodlesApp.business.home.home import home_bp
    from PratyushDoodlesApp.business.auth.auth import google_bp


    app.register_blueprint(cart_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(others_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(google_bp, url_prefix='/google_login')
    
    return app


app = create_app()
db = SQLAlchemy(app)