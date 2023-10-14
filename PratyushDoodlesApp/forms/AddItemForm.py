from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, NumberRange, URL, Optional, InputRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    images = StringField('Image URL', validators=[DataRequired()])
