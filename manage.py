import os

from flask_script import Manager

from app import create_app

app = create_app(os.getenv("APP_SETTINGS") or "config.development_config")
#manager = Manager(app)

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
