from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField, StringField, SubmitField
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
