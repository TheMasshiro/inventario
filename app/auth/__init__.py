from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="template/auth")

from app.auth import auth_routes  # noqa: E402, F401
