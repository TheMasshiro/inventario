from flask import Flask
from flask_login import LoginManager

from instance.config import Config

login = LoginManager()
login.login_view = "auth.login"  # type: ignore


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    login.init_app(app)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    from app.models import init_db

    init_db()

    from app.auth import auth_bp
    from app.errors import errors_bp
    from app.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)

    return app
