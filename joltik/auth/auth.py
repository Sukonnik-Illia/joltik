from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from joltik.config import config

cookie_transport = CookieTransport(cookie_name="crm", cookie_max_age=28800)

SECRET = config.secret


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
