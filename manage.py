import os

from flask_script import Manager, Server

from app import create_app

app = create_app(os.getenv("APP_SETTINGS") or "config.development_config")
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(host="0.0.0.0", port=5000, ssl_context=(".ssl/cert.pem", ".ssl/key.pem")),
)

if __name__ == "__main__":
    manager.run()
