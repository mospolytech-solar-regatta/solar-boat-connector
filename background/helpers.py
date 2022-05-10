import requests

import constants


def post(data: str):
    url = constants.HTTP_BASE + constants.URLEndpoints.STATE_POST
    requests.post(url, data=data, headers={'Content-type': 'application/json'})
