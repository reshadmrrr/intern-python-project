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


class TweeterUser:
    def __init__(self, username, password) -> None:
        res = NetworkRequest.post(
            endpoint="auth", body={"username": username, "password": password}
        )
        self._update_token(res["body"])

    def _update_token(self, res):
        self.access_token = res["access_token"] if "access_token" in res else ""
        self.refresh_token = res["refresh_token"] if "refresh_token" in res else ""
        self.token_type = res["token_type"] if "token_type" in res else ""

    def _refresh_token(self):
        res = NetworkRequest.post(
            endpoint="auth/token", body={"refresh_token": self.refresh_token}
        )
        self._update_token(res["body"])

    @time_logger
    def get_last_5_tweets(self):
        self.last_tweets = (
            NetworkRequest.get(
                endpoint="tweets",
                headers={
                    "Authorization": f"{self.token_type.capitalize()} {self.access_token}"
                },
            )["body"]
            if len(self.access_token) > 0
            else {}
        )
        return self.last_tweets

    def print_tweets(self):
        for r in self.last_tweets:
            print(
                f"({r['id']})  {r['author']['username']} at {r['created_at']}\n{r['text']}\n"
            )

    @time_logger
    @token_validate
    def post_tweet(self, tweet):
        return NetworkRequest.post(
            endpoint="tweets",
            headers={
                "Authorization": f"{self.token_type.capitalize()} {self.access_token}"
            },
            body={"text": tweet},
        )
