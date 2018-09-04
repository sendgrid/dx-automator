import requests
import json
import os
import pprint


def get_look(look_id):
    cid, cs, endpt = get_looker_credentials()
    looker_api = LookerApiHandler(endpt)
    looker_api.login(cid, cs)
    json_object = looker_api.run_look(look_id).json()
    looker_api.logout()
    return json_object


def get_looker_credentials():
    client_id = os.environ.get("LOOKER_CLIENT_ID")
    client_secret = os.environ.get("LOOKER_CLIENT_SECRET")
    endpoint = os.environ.get("SENDGRID_LOOKER")

    return client_id, client_secret, endpoint


class LookerApiHandler(object):
    def __init__(self, endpoint: str):
        self._token = None

        self.endpt = endpoint
        self.session = requests.session()

        self.dx_cache = None

    def login(self, client_id, client_secret):
        """Updates session with Looker token from given client credentials"""
        params = {"client_id": client_id,
                  "client_secret": client_secret}
        response = self.session.post("{}/login".format(self.endpt),
                                     params=params)
        self._token = response.json().get("access_token")
        self.session.headers.update(
            {"Authorization": "token {}".format(self._token)}
        )

    def run_look(self, look_id: int, result_format="json"):
        """Returns response from GET of specified look_id"""
        return self.session.get("{}/api/3.0/looks/{}/run/{}".format(
            self.endpt, look_id, result_format)
        )

    def logout(self):
        """Logout to revoke access token"""
        return self.session.delete("{}/api/3.0/logout".format(self.endpt))

    def __del__(self):
        self.logout()
