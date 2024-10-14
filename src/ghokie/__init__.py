import time
import requests
import jwt
import sys
from typing import TypedDict, NotRequired

def ready_headers(private_key: str, key_is_contents: bool, client_id: str) -> dict: # type: ignore
    """ Use the private key and client_id to create necessary headers """

    if key_is_contents:
        signing_key = private_key
    else:
        with open(private_key, 'rb') as private_key_file:
            signing_key = private_key_file.read()

    payload = {
        'iat': int(time.time()),       # Issued at time
        'exp': int(time.time()) + 600, # JWT expiration time (10 minutes maximum)
        'iss': client_id               # GitHub App's client ID
    }
    encoded_jwt = jwt.encode(payload, signing_key, algorithm='RS256')

    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {encoded_jwt}"
    }

def get_installation_id(app_name: str, headers: dict) -> str: # type: ignore
    """ Get the installation ID for the GitHub App """

    installations = requests.get(
        url='https://api.github.com/app/installations',
        headers=headers
    ).json()

    return [ installation['id'] for installation in installations if installation['app_slug'] == app_name ][0]

# https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#create-an-installation-access-token-for-an-app--parameters
class AccessTokenPermissions(TypedDict):
    contents: NotRequired[str]
    metadata: NotRequired[str]
    pull_requests: NotRequired[str]
    issues: NotRequired[str]
    administration: NotRequired[str]
    checks: NotRequired[str]
    deployments: NotRequired[str]
    pages: NotRequired[str]
    actions: NotRequired[str]
    packages: NotRequired[str]
    repository_hooks: NotRequired[str]
    repository_projects: NotRequired[str]
    vulnerability_alerts: NotRequired[str]
    secrets: NotRequired[str]
    security_events: NotRequired[str]
class AccessTokenBody(TypedDict):
    repositories: NotRequired[list[str]]
    repository_ids: NotRequired[list[int]]
    permissions: NotRequired[AccessTokenPermissions]

def get_access_token(
        app_name: str,
        private_key: str,
        client_id: str,
        key_is_contents: bool = False,
        body: AccessTokenBody = AccessTokenBody()
    ) -> str:
    """
    Return an access token based on parameters in <body: AccessTokenPermissions>
    or die trying
    """

    headers = ready_headers(private_key, key_is_contents, client_id)
    installation_id = get_installation_id(app_name, headers)

    try:
        response = requests.post(
            url=f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            json=body,
            headers=headers
        )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    response_json = response.json()

    if response.status_code not in range(200, 299):
        print(f"An error occurred: {response_json}")
        sys.exit(1)

    return response_json['token']
