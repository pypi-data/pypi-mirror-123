import logging
from typing import Optional

import requests
import urllib3

from racetrack_client.client.deploy import _get_deploy_request_headers
from racetrack_client.client_config.alias import resolve_lifecycle_url
from racetrack_client.client_config.auth import get_user_auth
from racetrack_client.client_config.io import load_client_config
from racetrack_client.manifest.validate import load_validated_manifest
from racetrack_client.utils.request import parse_response

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def show_logs(workdir: str, lifecycle_url: Optional[str], tail: int):
    """
    Show logs from fatman output
    :param workdir: directory with fatman.yaml manifest
    :param lifecycle_url: URL to Lifecycle API
    :param tail: number of recent lines to show
    """
    client_config = load_client_config()
    manifest = load_validated_manifest(workdir)
    lifecycle_url = resolve_lifecycle_url(client_config, lifecycle_url)
    user_auth = get_user_auth(client_config, lifecycle_url)
    logging.info(f'Retrieving logs of "{manifest.name}" fatman from {lifecycle_url}...')

    r = requests.get(
        f'{lifecycle_url}/api/v1/fatman/{manifest.name}/logs',
        params={'tail': tail},
        headers=_get_deploy_request_headers(user_auth),
        verify=False,
    )
    response = parse_response(r, 'Lifecycle response error')
    logs: str = response['logs']
    log_lines = len(logs.splitlines())
    logging.info(f'Recent logs of "{manifest.name}" fatman ({log_lines} lines):\n')
    print(logs)
