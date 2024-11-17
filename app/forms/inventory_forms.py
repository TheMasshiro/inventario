from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductForm(FlaskForm):
    product_name = StringField(
        "Product Name",
        validators=[
            DataRequired("Product name is required"),
            Length(
                min=3,
                message="Product name must be 3 characters long",
            ),
        ],
    )
    price = FloatField(
        "Price",
        default=0,
        validators=[
            Optional(),
            NumberRange(min=0, message="Price must not be negative"),
        ],
    )
    stock = IntegerField(
        "Stock",
        default=0,
        validators=[
            Optional(),
            NumberRange(min=0, message="Stock must not be negative"),
        ],
    )
    supplier_name = SelectField(
        "Supplier Name",
        choices=[],
        validators=[DataRequired("Supplier name is required")],
    )

    add_submit = SubmitField("Add Product")
    edit_submit = SubmitField("Save Changes")
    remove_submit = SubmitField("Remove Product")
