from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.models.user_models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("This field is required"),
            Length(
                min=8,
                max=20,
                message="Username must be between 8 and 20 characters long",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("This field is required"),
            Length(min=8, message="Password must be at least 8 characters long"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired("This field is required"),
            EqualTo("password", message="Passwords do not match"),
        ],
    )
    terms_and_conditions = BooleanField(
        "I agree to the",
        validators=[DataRequired("You must agree to terms and conditions")],
    )
    remember_me = BooleanField(default=True)
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User(username=username.data).get_user()
        if user is not None:
            raise ValidationError("Username is already taken")

    def validate_password(self, password):
        if not any(char.isupper() for char in password.data):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in password.data):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Password must contain at least one number")

        special_chars = '!@#$%^&*(),.?":{}|<>'
        if not any(char in special_chars for char in password.data):
            raise ValidationError(
                "Password must contain at least one special character"
            )


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired("This field is required")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired("This field is required")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log in")

    def validate_username(self, username):
        user = User(username=username.data).get_user()
        if user and not user.check_password(self.password.data):
            raise ValidationError("Incorrect Username or Password")

    def validate_password(self, password):
        user = User(username=self.username.data).get_user()
        if user and not user.check_password(password.data):
            raise ValidationError("Incorrect Username or Password")


class EditProfile(FlaskForm):
    old_password = PasswordField(
        "Old Password", validators=[DataRequired(message="This field is required")]
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="This field is required"),
            Length(min=8, message="Password must be at least 8 characters long"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="This field is required"),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Save Changes")

    def validate_old_password(self, old_password):
        from flask_login import current_user

        if not current_user.check_password(old_password.data):
            raise ValidationError("Incorrect password")

    def validate_new_password(self, field):
        if field.data == self.old_password.data:
            raise ValidationError("New password must be different from old password")

        if not any(char.isupper() for char in field.data):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in field.data):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in field.data):
            raise ValidationError("Password must contain at least one number")

        special_chars = '!@#$%^&*(),.?":{}|<>'
        if not any(char in special_chars for char in field.data):
            raise ValidationError(
                "Password must contain at least one special character"
            )


class EditStore(FlaskForm):
    store_name = StringField(
        validators=[
            DataRequired("This field is required"),
            Length(
                min=3,
                max=25,
                message="Store name must be between 8 and 25 characters long",
            ),
        ],
    )
    submit = SubmitField("Save Changes")
