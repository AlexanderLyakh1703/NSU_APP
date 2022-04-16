from flask import Response, redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

from app import basic_auth


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                "You could not be authenticated. Please refresh the page.",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            ),
        )


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


def create_admin(app):
    admin = Admin(
        app, index_view=MyAdminIndexView(), name="NSU_APP", template_mode="bootstrap4"
    )
    return admin
