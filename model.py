from decorators import time_logger, token_validate
from util import NetworkRequest


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
