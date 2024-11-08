from wtforms import StringField
from wtforms.validators import DataRequired


class ProductForm:
    product_name = StringField(
        "Username",
        validators=[
            DataRequired("This field is required"),
        ],
    )
