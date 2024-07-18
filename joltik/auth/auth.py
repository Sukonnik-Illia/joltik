from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from joltik.config import config

cookie_transport = CookieTransport(cookie_name="crm", cookie_max_age=28800)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
