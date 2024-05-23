from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, NumberRange, URL, Optional, InputRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    images = StringField('Image URL', validators=[DataRequired()])
    discount_percent = IntegerField('discount_percent', validators=[DataRequired(), NumberRange(min=0)])
    product_highlight = TextAreaField('product_highlight', validators=[Optional()])
    product_category = TextAreaField('product_category', validators=[Optional()])
    delete = TextAreaField('Delete Product ID:', validators=[Optional()])
    submit = SubmitField('Update Product')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if kwargs.get('obj'):
            self.name.data = kwargs['obj'].name
            self.description.data = kwargs['obj'].description
            self.price.data = kwargs['obj'].price
            self.stock_quantity.data = kwargs['obj'].stock_quantity
            images = ""
            for product_image in kwargs['obj'].product_images:
                images += product_image.picture_url+", "

            self.images.data = images
            self.discount_percent.data = kwargs['obj'].discount_percent
            self.product_highlight.data = kwargs['obj'].product_highlight
            self.product_category.data = kwargs['obj'].product_category
            self.delete.data = None
        elif kwargs.get('form'):
            self.initialize_from_request(kwargs['form'])    

    def initialize_from_request(self, request_form):
        self.name.data = request_form.get('name')
        self.description.data = request_form.get('description')
        self.price.data = float(request_form.get('price'))
        self.stock_quantity.data = float(request_form.get('stock_quantity'))
        self.images.data = request_form.get('images')
        self.discount_percent.data = float(request_form.get('discount_percent'))
        self.product_highlight.data = request_form.get('product_highlight')
        self.product_category.data = request_form.get('product_category')        
        self.delete.data = None


class DeleteProductForm(FlaskForm):
    delete_product_id = TextAreaField('Delete Product ID:', validators=[Optional()])    