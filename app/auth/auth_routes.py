from flask_login import login_required

from app.auth import auth_bp as auth
from app.auth.auth_manager import AuthManager


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    return AuthManager().logout_user()


@auth.route("/login", methods=["GET", "POST"])
def login():
    return AuthManager().login_user()


@auth.route("/register", methods=["GET", "POST"])
def register():
    return AuthManager().register_user()
