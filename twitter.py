import os
from typing import List, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import requests
import pathlib
from geocode import get_coordinates
from threading import Timer


@dataclass
class Friend:
    location: Tuple[float, float]
    name: str
    username: str


class TwitterException(Exception):
    pass


latest_uses = 0


def add_use():
    global latest_uses
    latest_uses += 1

    def delete_use():
        global latest_uses
        latest_uses -= 1
    Timer(60 * 15, delete_use).start()


def make_request(url: str, mark_as_use: bool = False):
    headers = {"Authorization": f"Bearer {os.getenv('BEARER')}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code not in [401, 404, 429, 500] and mark_as_use:
        add_use()
    return resp.json()


def get_user_id(username: str) -> str:
    req = make_request(f"https://api.twitter.com/2/users/by/username/{username}")
    if 'errors' in req and 'message' in req['errors'][0]:
        raise TwitterException(req['errors'][0]['message'])
    return req["data"]["id"]


def get_friends(username: str, count: int) -> List[Friend]:
    resp = make_request(f"https://api.twitter.com/2/users/{get_user_id(username)}/following?"
                        f"user.fields=location,name,username", mark_as_use=True)
    if 'status' in resp and resp["status"] == 429:
        raise TwitterException("Too Many Requests")
    if 'meta' in resp and 'result_count' in resp['meta'] and resp['meta']['result_count'] == 0:
        return []
    friends = []

    for user in list(filter(lambda u: "location" in u, resp["data"])):
        if coords := get_coordinates(user["location"]):
            friends.append(Friend(coords, user["name"], user["username"]))
            if len(friends) == count:
                break

    return friends


load_dotenv(pathlib.Path(__file__).parent.resolve().name + "/.env")
