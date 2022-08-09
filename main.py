from getpass import getpass
import traceback


from util import TweeterUser


def main():
    print("Please login to your account")
    username = input("Username: ")
    password = getpass()
    print("Logging in ...")
    try:
        user = TweeterUser(username=username, password=password)
        if hasattr(user, "access_token") and len(user.access_token) > 0:
            print("Login successful ...")
        else:
            print("Login failed ...")
        print("Checking recent tweets ...")
        user.get_last_5_tweets()
    except:
        print(traceback.format_exc())
        print("Login failed ...")


if __name__ == "__main__":
    main()
