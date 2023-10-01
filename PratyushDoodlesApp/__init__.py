from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    app.secret_key = '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'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    return app


app = create_app()
db = SQLAlchemy(app)

from PratyushDoodlesApp.business.cart import *
from PratyushDoodlesApp.business.auth import *
from PratyushDoodlesApp.business.shop import *
from PratyushDoodlesApp.business.payments import *
from PratyushDoodlesApp.business.others import *
from PratyushDoodlesApp.business.home import *
from PratyushDoodlesApp.models.ProductModel import *
from PratyushDoodlesApp.models.UserModel import *