"""
The CTA API appears to use non-standard security protocols. Or, at least, 
writing it that way makes it sounds like I know what I'm talking about. Using
a standard `requests.get(url)` returns the an error that includes:

    SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:1006)')

But with Postman I'm able to verify that the CTA Train Locations API works. So, 
from the StackOverflow post below, I was able to find the code used here to fix
the issue. Copy paste, baby.

https://stackoverflow.com/a/76217135
"""

import os
import json

from dotenv import load_dotenv
from urllib3.util import create_urllib3_context
from urllib3 import PoolManager
from requests.adapters import HTTPAdapter
from requests import Session
from urllib.parse import urljoin


load_dotenv()


class AddedCipherAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = create_urllib3_context(ciphers=":HIGH:!DH:!aNULL")
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=ctx
        )


class CTA_API:
    def __init__(self):
        self.base_url = "https://lapi.transitchicago.com"
        self.locations_api = "/api/1.0/ttpositions.aspx"

        self.https = Session()
        self.https.mount(self.base_url, AddedCipherAdapter())

    
    def get_locations(self):
        # Train lines must be specified as follows
        train_lines = [
            # "red",
            # "blue",
            "p",
            # "org",
            # "brn",
            "y",
            "g",
            # "pink",
            ]
        params = {
            "key":  os.environ.get("CTA_TRAIN_TRACKER_API_KEY"),
            "rt":   ",".join(train_lines),
            "outputType": "JSON",
        }
        api_url = urljoin(self.base_url, self.locations_api)
        response = self.https.get(api_url, params=params)
        content = json.loads(response.text)
        return content