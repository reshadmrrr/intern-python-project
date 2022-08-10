from time import time


def time_logger(function):
    def wrapper(*args, **kwargs):
        start = time()
        fn = function(*args, **kwargs)
        end = time()
        print(f"(time taken: {end - start} ms)")
        return fn

    return wrapper


def token_validate(function):
    def wrapper(self, *args, **kwargs):
        res = function(self, *args, **kwargs)
        if res["code"] == 401:
            print("Access token's expired, getting a new one...")
            self._refresh_token()
            res = function(self, *args, **kwargs)
        return res

    return wrapper
