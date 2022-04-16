import os
from sys import platform

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class config(object):
    # Секретный ключ
    SECRET_KEY = os.getenv("SECRET_KEY") or "random_string"

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


class production_config(config):
    DEBUG = False


class development_config(config):
    DEVELOPMENT = True
    DEBUG = True
