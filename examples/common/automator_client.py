import os

from python_http_client import Client


def get_automator_ip():
    if 'DX_IP' in os.environ:
        return os.environ['DX_IP']

    return os.popen('docker-machine ip dx-automator-dev').read().strip()


client = Client(host="http://{}".format(get_automator_ip()))
