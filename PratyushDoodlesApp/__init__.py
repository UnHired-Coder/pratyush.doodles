from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO
import razorpay
from flask_login import LoginManager



def create_app():
    app = Flask(__name__)

    app.secret_key = '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'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['RAZORPAY_KEY_ID'] = 'rzp_live_iTOaD3Yk22nsGw'
    app.config['RAZORPAY_KEY_SECRET'] = 'slVy5AwVnKx7fdDopZCYNsRL'

    return app


app = create_app()
# socketio = SocketIO(app, async_mode = None)
db = SQLAlchemy(app)
razorpayClient = razorpay.Client(auth = (app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))
razorpayClient.set_app_details({"title" : "Pratyush Doodles", "version" : "1.0"})

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from PratyushDoodlesApp.business.cart import *
from PratyushDoodlesApp.business.auth import *
from PratyushDoodlesApp.business.shop import *
from PratyushDoodlesApp.business.checkout import *
from PratyushDoodlesApp.business.others import *
from PratyushDoodlesApp.business.home import *
from PratyushDoodlesApp.models.ProductModel import *
from PratyushDoodlesApp.models.UserModel import *