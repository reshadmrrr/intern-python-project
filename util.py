import json
import traceback
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import os
from dotenv import load_dotenv

from decorators import time_logger, token_validate

load_dotenv()


"""
TODO: Write whatever class or function you may need
but, don't use any third party library
feel free to make any changes in the given class and its methods' arguments or implementation as you see fit
"""


BASE_URL = os.getenv("API")


class NetworkRequest:
    @staticmethod
    def _request(req):
        req.add_header("Content-Type", "application/json")
        res = {}
        try:
            with urlopen(req) as r:
                # print(r)
                body = r.read().decode("utf-8")
                res["body"] = json.loads(body)
                res["code"] = r.status
                # print(r.status)
                # print(json.loads(body))
        except Exception as e:
            res["code"] = e.code
            # print(e.code)
        # print(res["code"])
        return res

    @staticmethod
    def get(endpoint="", headers={}):
        return NetworkRequest._request(
            Request(url=BASE_URL + endpoint, method="GET", headers=headers)
        )

    @staticmethod
    def post(endpoint="", headers={}, body={}):
        return NetworkRequest._request(
            Request(
                url=BASE_URL + endpoint,
                headers=headers,
                data=bytes(json.dumps(body), encoding="utf-8"),
                method="POST",
            )
        )

    @staticmethod
    def put():
        pass

    @staticmethod
    def delete():
        pass
