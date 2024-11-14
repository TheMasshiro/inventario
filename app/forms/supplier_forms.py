from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length


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
