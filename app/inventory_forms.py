from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField, SubmitField
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
            NumberRange(min=0, message="Price must be greater than or equal to 0"),
        ],
    )
    quantity = IntegerField(
        "Quantity",
        default=0,
        validators=[
            Optional(),
            NumberRange(min=0, message="Quantity must be greater than or equal to 0"),
        ],
    )
    supplier_name = StringField(
        "Supplier Name",
        validators=[
            DataRequired("Supplier name is required"),
            Length(
                min=3,
                message="Supplier name must be 3 characters long",
            ),
        ],
    )
    add_submit = SubmitField("Add Product")
    edit_submit = SubmitField("Save Changes")
    remove_submit = SubmitField("Remove Product")
