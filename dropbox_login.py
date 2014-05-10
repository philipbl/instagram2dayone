#!/usr/bin/env python

# YOU NEED TO INSERT YOUR APP KEY AND SECRET BELOW!
# Go to dropbox.com/developers/apps to create an app.

import webbrowser
from dropbox import client, rest, session
import pickle
import yaml

def load_config(config_name):
    with open(config_name) as f:
        return yaml.load(f)


def save_config(config_name, config):
    with open(config_name, 'w') as f:
        f.write(yaml.dump(config, default_flow_style=True))


def _get_request_token(app_key, app_secret, access_type):
    sess = session.DropboxSession(app_key, app_secret, access_type)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)

    webbrowser.open(url)
    print "Press enter after allowing application..."
    raw_input()

    return request_token


def _get_access_token(app_key, app_secret, access_type):
    request_token = _get_request_token(app_key, app_secret, access_type)
    sess = session.DropboxSession(app_key, app_secret, access_type)
    access_token = sess.obtain_access_token(request_token)

    return (access_token.key, access_token.secret)


def get_client():
    config_name = "dropbox_config.yaml"

    config = load_config(config_name)
    app_key = config['app_key']
    app_secret = config['app_secret']
    access_type = config['access_type']
    key = config.get('access_key', None)
    secret = config.get('access_secret', None)

    if key is None or secret is None:
        key, secret = _get_access_token(app_key, app_secret, access_type)

        # Store access tokens for later
        config['access_key'] = key
        config['access_secret'] = secret

        save_config(config_name, config)

    sess = session.DropboxSession(app_key, app_secret, access_type)
    sess.set_token(key, secret)

    dropbox_client = client.DropboxClient(sess)
    return dropbox_client


def main():
    # Demo if started run as a script...
    # Just print the account info to verify that the authentication worked:
    print 'Getting account info...'
    dropbox_client = get_client()
    account_info = dropbox_client.account_info()
    print 'linked account:', account_info


if __name__ == '__main__':
    main()
