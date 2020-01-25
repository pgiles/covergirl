import requests
import json
import fileutil
import os
import logging
log = logging.getLogger(__name__)


class Spotify:

    def __init__(self):
        pass

    encoded_credential = fileutil.read_file("..{}encoded_credential".format(os.sep))
    token_path = "..{}token".format(os.sep)
    access_token = fileutil.read_file(token_path)
    api_root = 'https://api.spotify.com/v1/'
    headers = {'Authorization': 'Bearer %s' % access_token,
               'Accept': 'application/json',
               'Content-Type': 'application/json'
               }
    default_params = {'limit': 2}

    def artist_info(self, artist_name):
        log.debug("Fetching artist info for: %s", artist_name)

        params = {'q': artist_name, 'type': 'artist'}
        return self.call_api(params)

    def album_info(self, artist_name, album_name):
        log.debug("Fetching album info for: %s %s", artist_name, album_name)

        params = {'q': "artist: %s album: %s" % (artist_name, album_name), 'type': 'album'}
        payload = self.call_api(params)
        if len(payload['albums']['items']) == 0:
            results = self.call_api({'q': album_name, 'type': 'album'})
            for itm in results['albums']['items']:
                if itm['name'] == artist_name:
                    return results
        else:
            return payload

    def call_api(self, params):
        params.update(self.default_params)
        resp = requests.get(self.api_root+'search', params=params, headers=self.headers)

        if resp.status_code == 200:
            return json.loads(resp.content)
        elif resp.status_code == 401:
            log.info('Refreshing token...')
            self.login()
        else:
            log.error("%s %s", resp.status_code, resp.text)
            return None

    def login(self):
        headers = {'Authorization': 'Basic %s' % self.encoded_credential}
        data = {'grant_type': 'client_credentials'}
        resp = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
        if resp.status_code == 200:
            json_string = json.loads(resp.content)
            # store access token
            fileutil.write_file(self.token_path, str(json_string['access_token']))
        else:
            log.error("%s %s", resp.status_code, resp.text)

    @staticmethod
    def handle_client_error(e):
        if e.response['Error']:
            print(e.response['Error'])
        else:
            print("Unexpected error: %s" % e)
        return exit(1)
