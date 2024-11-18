from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


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
