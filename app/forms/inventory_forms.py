from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
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


class SupplierForm(FlaskForm):
    company_name = StringField(
        "Company Name",
        validators=[
            DataRequired("Company name is required"),
            Length(
                min=4,
                message="Company name must be 4 characters long",
            ),
        ],
    )
    supplier_name = StringField(
        "Supplier Name",
        validators=[
            DataRequired("Supplier name is required"),
            Length(
                min=4,
                message="Supplier name must be 4 characters long",
            ),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Email is required"),
        ],
    )
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired("Phone number is required"),
            Length(
                min=11,
                max=11,
                message="Phone number must be 11 digits long.",
            ),
        ],
    )
    status = SelectField(
        "Status",
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",
        validators=[DataRequired("Status is required")],
    )

    add_submit = SubmitField("Add Supplier")
    edit_submit = SubmitField("Save Changes")
    remove_submit = SubmitField("Remove Supplier")

    def validate_supplier_name(self, supplier_name):
        supplier = supplier_name.data

        if not supplier.isalpha():
            raise ValidationError("Supplier name must contain only letters.")

    def validate_phone(self, phone):
        phone_number = phone.data

        number_format = phone_number[0:2]
        if number_format != "09" and number_format != "63":
            raise ValidationError("Phone number must start with '09' or '63'.")
