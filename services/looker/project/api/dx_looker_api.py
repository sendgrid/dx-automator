import requests
import json
import os
import pprint


def parse_dx_look_json(json_dict: dict):
    pprint.pprint(json_dict)


class DxLookerApi(object):
    def __init__(self, client_id: str, client_secret: str, endpoint: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = None

        self.endpt = endpoint
        self.session = requests.session()

    def authenticate(self):
        """Updates session with Looker token from given client credentials"""
        params = {"client_id": self._client_id,
                  "client_secret": self._client_secret}
        response = self.session.post("{}/login".format(self.endpt),
                                     params=params)
        self._token = response.json().get("access_token")
        self.session.headers.update(
            {"Authorization": "token {}".format(self._token)}
        )

    def run_look(self, look_id: str, result_format="json"):
        """Returns response from GET of specified look_id"""
        return looker_api.session.get("{}/api/3.0/looks/{}/run/{}".format(
            self.endpt, look_id, result_format)
        )


if __name__ == "__main__":
    sg_client_id = os.environ.get("LOOKER_CLIENT_ID")
    sg_client_secret = os.environ.get("LOOKER_CLIENT_SECRET")
    sg_endpoint = os.environ.get("SENDGRID_LOOKER")
    looker_api = DxLookerApi(sg_client_id, sg_client_secret, sg_endpoint)
    looker_api.authenticate()
    json_object = looker_api.run_look("4405").json()
    parse_dx_look_json(json_object)

