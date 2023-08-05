from typing import Optional

from racetrack_client.client_config.alias import _resolve_short_lifecycle_url, resolve_lifecycle_url
from racetrack_client.client_config.io import load_client_config, save_client_config
from racetrack_client.client_config.client_config import ClientConfig

RT_USER_AUTH_HEADER = "X-Racetrack-User-Auth"


class AuthError(RuntimeError):
    def __init__(self, cause: str):
        super().__init__()
        self.cause = cause

    def __str__(self):
        return f'authentication error: {self.cause}'


def set_user_auth(client_config: ClientConfig, lifecycle_url: str, user_auth: str):
    """
    You need to save the resulting config if you want to make changes persist
    """
    lifecycle_url = resolve_lifecycle_url(client_config, lifecycle_url)

    if len(user_auth) == 0:
        if lifecycle_url in client_config.user_auths:
            del client_config.user_auths[lifecycle_url]
        else:
            raise RuntimeError(f'Missing {lifecycle_url} in Racetrack logged servers')
    else:
        client_config.user_auths[lifecycle_url] = user_auth


def get_user_auth(client_config: ClientConfig, lifecycle_url: Optional[str]) -> str:
    """
    lifecycle_url can refer to alias, or URL
    """

    if lifecycle_url in client_config.user_auths:
        return client_config.user_auths[lifecycle_url]

    short_url = _resolve_short_lifecycle_url(client_config, lifecycle_url)

    if short_url in client_config.user_auths:
        return client_config.user_auths[short_url]

    raise AuthError(f"missing login. You need to do: racetrack login {lifecycle_url} <token>")
