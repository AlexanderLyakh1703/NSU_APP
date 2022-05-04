from config import oauth_config as auconf
from requests_oauthlib import OAuth2Session


def get_auth(state=None, token=None):
    if token:
        return OAuth2Session(auconf.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            auconf.CLIENT_ID, state=state, redirect_uri=auconf.REDIRECT_URI
        )
    return OAuth2Session(
        auconf.CLIENT_ID, redirect_uri=auconf.REDIRECT_URI, scope=auconf.SCOPE
    )


def authorization():
    service = get_auth()
    return service.authorization_url(auconf.AUTH_BASE_URL)


def get_token(state, auth_url):
    service = get_auth(state=state)
    token = service.fetch_token(
        auconf.TOKEN_URL,
        client_secret=auconf.CLIENT_SECRET,
        authorization_response=auth_url,
    )
    return token


def get_userinfo(token):
    service = get_auth(token=token)
    req_data = service.get(
        "https://sso.nsu.ru/auth/realms/NSU/protocol/openid-connect/userinfo"
    ).json()
    req_data["groups"] = {
        (t := g.rsplit("/", 2)[1:])[0]: t[1] for g in req_data["groups"]
    }
    return req_data
