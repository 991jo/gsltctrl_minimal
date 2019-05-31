import argparse

from sys import exit
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from json import dumps, loads

BASEURL = "https://api.steampowered.com/IGameServersService/"


def is_uint32(value):
    return isinstance(value, int) and value >= 0 and value < 2**32


def is_uint64(value):
    return isinstance(value, int) and value >= 0 and value < 2**64


def is_str(value):
    return isinstance(value, str)


def load_apikey(filename="APIKEY"):
    try:
        with open(filename) as f:
            return f.readline().strip()
    except FileNotFoundError:
        print("APIKEY file not found.")
        exit(1)


def handle_get(args):
    servers = GSLT.get_account_list()

    for server in servers:
        if server["memo"] == args.memo:
            if server["is_expired"]:
                steamid = int(server["steamid"])
                resp = GSLT.reset_login_token(steamid)
                login_token = resp["response"]["login_token"]
                print(login_token)
            else:
                print(server["login_token"])
            return
    resp = GSLT.create_account(args.appid, args.memo)
    print(resp["response"]["login_token"])


class GameServersService():
    def __init__(self, apikey, baseurl=BASEURL):
        """
        Creates a GameServersService object.

        :param str apikey: your API key
        :param str baseurl: the URL you want to use. Defaults to the regular
                            url steam provides.
        """
        self.apikey = apikey
        self.baseurl = baseurl

    def make_request(self, url, data, method="GET"):
        r = Request(self.baseurl + url + "?" + self.encode_data(data),
                    method=method)
        resp = urlopen(r)
        json = resp.read().decode("utf-8")
        return loads(json)

    def get_request(self, url, data={}):
        return self.make_request(url, data, "GET")

    def post_request(self, url, data={}):
        return self.make_request(url, data, "POST")

    def encode_data(self, data):
        """
        Encodes the given data into an urlencoded json as a utf-8 encoded
        bytestring.

        :param dict(str: str) data: the data needed for the request
        :returns bytes: a bytestring
        """

        json = dumps(data)
        urlencoded = urlencode({"key": self.apikey, "input_json": json})
        return urlencoded  # .encode("utf-8")

    def get_account_list(self):
        """Returns a list of all registered tokens."""
        url = "GetAccountList/v1"
        return self.get_request(url)["response"]["servers"]

    def create_account(self, appid, memo=""):
        """
        Creates a new token.

        :param int appid: the AppID of the game (not the server)
        :param str memo: the Memo for the new token.
        """
        assert is_uint32(appid)
        assert is_str(memo)
        url = "CreateAccount/v1"
        return self.post_request(url, {"appid": appid, "memo": memo})

    def reset_login_token(self, steamid):
        """
        Resets/Regenerates the token for the given steamid.

        :param steamid: the steamid of the server, a unsignet 64 bit integer.
        :returns: a dict containing the new token.
        """
        assert is_uint64(steamid)
        url = "ResetLoginToken/v1"
        return self.post_request(url, {"steamid": steamid})

    def query_login_token(self, login_token):
        assert is_str(login_token)
        url = "QueryLoginToken/v1"
        return self.get_request(url, {"login_token": login_token})


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("appid", type=int)
    argparser.add_argument("memo", type=str)

    args = argparser.parse_args()

    APIKEY = load_apikey()
    GSLT = GameServersService(APIKEY)

    handle_get(args)
