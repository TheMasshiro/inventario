from flask import Blueprint

main_bp = Blueprint("main", __name__, template_folder="template/main")

from app.main import main_routes  # noqa: E402, F401
