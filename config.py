import os
from sys import platform

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class config(object):
    # Секретный ключ
    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(24)

    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    DEBUG = False
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True

    FLASK_ADMIN_SWATCH = "cerulean"

    # Вход в панель админа
    BASIC_AUTH_USERNAME = "admin"
    BASIC_AUTH_PASSWORD = os.getenv("ADMIN_PASSWORD") or "admin"

    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = ".flask_session"


class production_config(config):
    DEBUG = False


class development_config(config):
    DEVELOPMENT = True
    DEBUG = True


# Test Google OAuth2
class oauth_config(object):
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "https://nsuapp.herokuapp.com/callback"

    # OAuth endpoints given in the Google API documentation
    AUTH_BASE_URL = "https://sso.nsu.ru/auth/realms/NSU/protocol/openid-connect/auth"
    TOKEN_URL = "https://sso.nsu.ru/auth/realms/NSU/protocol/openid-connect/token"
    SCOPE = [
        "openid",
        "profile",
        "groups",
        "email",
    ]


class api_config(object):
    TABLE_TOKEN = os.getenv("TABLE_TOKEN")
