#!/usr/bin/env python3
import sys
import os
import argparse
import json

from ghokie import get_access_token

def main():
    """ Parse arguments and call get_access_token """
    parser = argparse.ArgumentParser(
                        prog='GH App Application Access token generator',
                        description="Generate a GitHub App Access Token with your App's private key and client ID",
                        usage='All options except --key-is-contents are required, but can also come from environment variables (GH_APP_NAME, GH_PRIVATE_KEY, GH_CLIENT_ID, GH_KEY, GH_KEY_IS_CONTENTS)',
                        )

    parser.add_argument('--app-name', '-a', required=False)
    parser.add_argument('--private-key', '-k', required=False)
    parser.add_argument('--client-id', '-c', required=False)
    parser.add_argument('--organisation', '-o', required=False)
    parser.add_argument('--key-is-contents', '-s', help="When passed --private-key is treated as the SSH key string itself, else it's a path", required=False, action='store_true')
    parser.add_argument('--body', '-b', help="JSON body to pass to the access token request", required=False)
    args = parser.parse_args()

    app_name = args.app_name or os.getenv('GH_APP_NAME')
    private_key = args.private_key or os.getenv('GH_PRIVATE_KEY')
    client_id = args.client_id or os.getenv('GH_CLIENT_ID')
    organisation = args.organisation or os.getenv('GH_ORGANISATION')
    key_is_contents = args.key_is_contents or os.getenv('GH_KEY_IS_CONTENTS') != None
    body = json.loads(args.body or os.getenv('GHOKIE_BODY', '{}'))

    if not app_name or not private_key or not client_id or not organisation:
        print("Please provide all the required arguments or set the environment variables")
        sys.exit(1)

    print(get_access_token(app_name, private_key, client_id, organisation, key_is_contents, body))

if __name__ == '__main__':
    main()
