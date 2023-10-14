from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, NumberRange, URL, Optional, InputRequired


class ShippingAddressForm(FlaskForm):
    recipient_name = StringField('Recipient Name', validators=[InputRequired()])
    address_line1 = StringField('Address Line 1', validators=[InputRequired()])
    address_line2 = StringField('Address Line 2')
    city = StringField('City', validators=[InputRequired()])
    state = StringField('State', validators=[InputRequired()])
    postal_code = StringField('Postal Code', validators=[InputRequired()])
    country = StringField('Country', validators=[InputRequired()])
    submit = SubmitField('Submit')
