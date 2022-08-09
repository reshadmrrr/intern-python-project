import json
import traceback
from urllib.request import Request, urlopen
import os
from dotenv import load_dotenv


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
                # res["code"] = r.status
        except:
            print(traceback.format_exc())
        return res["body"]

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
        # print(res)
        self.access_token = res["access_token"]
        self.refresh_token = res["refresh_token"]
        self.token_type = res["token_type"]

    def get_last_5_tweets(self):
        res = NetworkRequest.get(
            endpoint="tweets",
            headers={
                "Authorization": f"{self.token_type.capitalize()} {self.access_token}"
            },
        )
        for r in res:
            print(
                f"({r['id']})  {r['author']['username']} at {r['created_at']}\n{r['text']}\n"
            )
