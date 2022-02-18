import os
from typing import List, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import requests
import pathlib
from geocode import get_coordinates


@dataclass
class Friend:
    location: Tuple[float, float]
    name: str
    username: str


def make_request(url: str):
    headers = {"Authorization": f"Bearer {os.getenv('BEARER')}"}
    return requests.get(url, headers=headers).json()


def get_user_id(username: str) -> str:
    return make_request(f"https://api.twitter.com/2/users/by/username/{username}")["data"]["id"]


def get_friends(username: str, count: int) -> List[Friend]:
    resp = make_request(f"https://api.twitter.com/2/users/{get_user_id(username)}/following?"
                        f"user.fields=location,name,username")
    friends = []
    for user in list(filter(lambda u: "location" in u, resp["data"])):
        if coords := get_coordinates(user["location"]):
            friends.append(Friend(coords, user["name"], user["username"]))
            if len(friends) == count:
                break

    return friends


load_dotenv(pathlib.Path(__file__).parent.resolve().name + "/.env")
