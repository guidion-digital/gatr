# Rationale

Personal Access Tokens are used in automation because they're easy to generate. This either poses a security risk (long lived tokens, generated by hand), or a burdon and security risk (regenerating every n days, by hand).

In order to make tokens you can use with the Github API easier to generate, I created this simple script. It's based on the [JWT token generator example](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app#example-using-python-to-generate-a-jwt), and simply adds some code to go a little further and generate a new application token.

This is the middle part to a fully automated token refresh set up:

1. [Create a Github App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) with the permissions your automation (token) will need
1. Use this script to generate an application access token
1. Push this new token to wherever it's needed (CI/CD?)

You will want to generate and push new tokens around every 30 or 40 minutes, since they expire automatically after 60 minutes.

# Installation

`pip install git+https://github.com/guidion-digital/ghokie.git`

# Usage

> [!NOTE]
The `--key-is-contents` flag will make the script treat `--private-key` as the string contents of the PEM file, rather than a path to the file.

Either as a module:

```python
#!/usr/bin/env python3

from ghokie import get_access_token

print(get_access_token(
  app_name='repoaccessbot',
  private_key='location-of-private-key.pem',
  client_id='client_id'))
```

or from the CLI:

```python
./ghokie-cli \
  -a 'repoaccessbot' \
  -k 'location-of-private-key.pem' \
  -c 'client_id'
```

When calling from the CLI, you can instead supply the options via the environment variables:

- `GH_APP_NAME`
- `GH_PRIVATE_KEY`
- `GH_CLIENT_ID`
- `GH_KEY_IS_CONTENTS`
