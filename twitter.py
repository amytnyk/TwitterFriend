import os
import random
from typing import List, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import requests

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


def get_friends(username: str) -> List[Friend]:
    resp = make_request(f"https://api.twitter.com/2/users/{get_user_id(username)}/following?"
                        f"user.fields=location,name,username")
    users_with_location = list(filter(lambda user: "location" in user, resp["data"]))
    users = random.sample(users_with_location, min(len(users_with_location), 6))
    return list(filter(lambda x: x.location,
                       [Friend(get_coordinates(user["location"]), user["name"], user["username"])
                        for user in users if "location" in user]))


load_dotenv()
