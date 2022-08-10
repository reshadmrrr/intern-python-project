from getpass import getpass
from pyjokes import get_joke
import time
import traceback


from util import TweeterUser


def main():
    print("Please login to your account")
    username = input("Username: ")
    password = getpass()
    print("Logging in ...")
    try:
        user = TweeterUser(username=username, password=password)
        if len(user.access_token) > 0:
            print("Login successful ...")
        else:
            print("Login failed ...")
        print("Checking recent tweets ...")
        tweets = user.get_last_5_tweets()
        user.print_tweets()
        distinct_tweets = set([t["text"] for t in tweets])
        length = len(distinct_tweets)
        while length + 10 > len(distinct_tweets):
            new_tweet = get_joke()
            if not new_tweet in distinct_tweets:
                distinct_tweets.add(new_tweet)
                print("Posting tweet ..,")
                print(new_tweet)
                user.post_tweet(tweet=new_tweet)
                print("Posted tweet ..., Sleeping 1 minute now...")
                time.sleep(60)
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
