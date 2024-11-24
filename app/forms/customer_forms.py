from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class CustomerForm(FlaskForm):
    customer_name = StringField(
        "Customer Name",
        validators=[
            DataRequired("Customer name is required"),
            Length(
                min=3,
                message="Customer name must be 3 characters long",
            ),
        ],
    )

    add_submit = SubmitField("Add Customer")
    edit_submit = SubmitField("Save Changes")
    remove_submit = SubmitField("Remove Customer")


class PurchaseForm(FlaskForm):
    product_id = HiddenField()

    customer_name = SelectField(
        "Customer Name",
        choices=[],
        validators=[
            DataRequired("Customer name is required"),
        ],
    )

    quantity = IntegerField(
        "Quantity",
        default=0,
        validators=[
            DataRequired("Quantity is required"),
            NumberRange(min=0, message="Quantity cannot be less than 0"),
        ],
    )

    purchase_submit = SubmitField("Purchase")
