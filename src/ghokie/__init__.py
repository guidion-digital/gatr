import time
import requests
import jwt

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

def get_access_token(app_name: str, private_key: str, client_id: str, key_is_contents: bool = False) -> str:
    headers = ready_headers(private_key, key_is_contents, client_id)
    installation_id = get_installation_id(app_name, headers)

    try:
        response = requests.post(
            url=f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers=headers
        )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    return response.json['token']
