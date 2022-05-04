from flask import Flask
from flask_basicauth import BasicAuth
from flask_session import Session

basic_auth = BasicAuth()


def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(config_env or "config")
    basic_auth.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/")

    from .admin import create_admin

    admin = create_admin(app)
    sess = Session(app)
    return app
