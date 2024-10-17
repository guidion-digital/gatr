# Github-App Application Token Rotator

# Rationale

Personal Access Tokens are used in automation because they're easy to generate. This either poses a security risk (long lived tokens, generated by hand), or a burdon and security risk (regenerating every n days, by hand).

In order to make tokens you can use with the Github API easier to generate, I created this simple script. It's based on the [JWT token generator example](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app#example-using-python-to-generate-a-jwt), and simply adds some code to go a little further and generate a new application token.

This is the middle part to a fully automated token refresh set up:

1. [Create a Github App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) with the permissions your automation (token) will need
1. Use this script to generate an application access token
1. Push this new token to wherever it's needed (CI/CD?)

You will want to generate and push new tokens around every 40 or 50 minutes, since they expire automatically after 60 minutes.

# Installation

`pip install git+https://github.com/guidion-digital/gatr.git`

or if you don't have `git` available on the system:

`pip install https://github.com/guidion-digital/gatr.git/archive/refs/heads/master.zip`

# Usage

> [!NOTE]
The `--key-is-contents` flag will make the script treat `--private-key` as the string contents of the PEM file, rather than a path to the file.

Either as a module:

```python
#!/usr/bin/env python3

from gatr import get_access_token

print(get_access_token(
  app_name='repoaccessbot',
  private_key='location-of-private-key.pem',
  client_id='client_id'),
  organisation='gh_org_name')
```

or from the CLI:

```python
./gatr-cli \
  -a 'repoaccessbot' \
  -k 'location-of-private-key.pem' \
  -c 'client_id' \
  -o 'github_org_name'
```

`--body` (`-b`) is optional, and consists of the "body parameters" documented [here](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#create-an-installation-access-token-for-an-app--parameters):

```json
{
  "repositories": [string],
  "repository_ids": [string],
  "permissions": {
      "contents": string,
      "metadata": string,
      "pull_requests": string,
      "issues": string,
      "administration": string,
      "checks": string,
      "deployments": string,
      "pages": string,
      "actions": string,
      "packages": string,
      "repository_hooks": string,
      "repository_projects": string,
      "vulnerability_alerts": string,
      "secrets": string,
      "security_events": string,
  }
}
```

When calling from the CLI, you can instead supply the options via the environment variables:

- `GH_APP_NAME`
- `GH_PRIVATE_KEY`
- `GH_CLIENT_ID`
- `GH_ORGANISATION`
- `GH_KEY_IS_CONTENTS`
- `GATR_BODY`
