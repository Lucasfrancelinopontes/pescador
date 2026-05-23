import os
from pathlib import Path

from flask import Flask, session
from jinja2 import ChoiceLoader, FileSystemLoader
from dotenv import load_dotenv


def create_app() -> Flask:
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static",
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    package_dir = Path(__file__).resolve().parent
    root_dir = package_dir.parent
    app.jinja_loader = ChoiceLoader(
        [
            FileSystemLoader(package_dir / "templates"),
            FileSystemLoader(root_dir / "templates"),
        ]
    )

    from app.auth.routes import bp as auth_bp
    from app.routes.errors import bp as errors_bp
    from app.routes.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    @app.context_processor
    def inject_globals() -> dict:
        return {"current_user_email": session.get("user_email")}

    return app
