#!/usr/bin/env python3
import sys
import time
import requests
import jwt
import os
import argparse

def ready_headers(private_key: str, key_is_contents: bool, client_id: str) -> dict:
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

def get_installation_id(app_name: str, headers: dict) -> str:
    """ Get the installation ID for the GitHub App """

    installations = requests.get(
        url='https://api.github.com/app/installations',
        headers=headers
    ).json()

    return [ installation['id'] for installation in installations if installation['app_slug'] == app_name ][0]

def get_access_token(app_name: str, private_key: str, client_id: str, key_is_contents: bool) -> str:
    headers = ready_headers(private_key, key_is_contents, client_id)
    installation_id = get_installation_id(app_name, headers)

    access_tokens = requests.post(
        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers=headers
    ).json()

    return access_tokens['token']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='GH App Application Access token generator',
                        description="Generate a GitHub App Access Token with your App's private key and client ID",
                        usage='All options except --key-is-contents are required, but can also come from environment variables (GH_APP_NAME, GH_PRIVATE_KEY, GH_CLIENT_ID, GH_KEY, GH_KEY_IS_CONTENTS)',
                        )

    parser.add_argument('--app-name', '-a', required=False)
    parser.add_argument('--private-key', '-k', required=False)
    parser.add_argument('--client-id', '-c', required=False)
    parser.add_argument('--key-is-contents', '-s', help="When passed --private-key is treated as the SSH key string itself, else it's a path", default=False, required=False, action='store_true')
    args = parser.parse_args()

    app_name = args.app_name or os.getenv('GH_APP_NAME')
    private_key = args.private_key or os.getenv('GH_PRIVATE_KEY')
    client_id = args.client_id or os.getenv('GH_CLIENT_ID')
    key_is_contents = args.key_is_contents or os.getenv('GH_KEY_IS_CONTENTS') != None

    if not app_name or not private_key or not client_id:
        print("Please provide all the required arguments or set the environment variables")
        sys.exit(1)

    print(get_access_token(app_name, private_key, client_id, key_is_contents))
