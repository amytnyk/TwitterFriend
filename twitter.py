from typing import List, Optional
from dataclasses import dataclass
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import requests


@dataclass
class Friend:
    latitude: float
    longitude: float
    name: str
    username: str


def make_request(url: str):
    headers = {
        "Authorization": "Bearer "
    }
    return requests.get(url, headers=headers).json()


def get_user_id(username: str) -> str:
    return make_request(f"https://api.twitter.com/2/users/by/username/{username}")["data"]["id"]


def get_coordinates(location: str) -> Optional[tuple[float, float]]:
    geolocator = Nominatim(user_agent="TwitterFriend")
    geocode = RateLimiter(geolocator.geocode)
    location = geocode(location)
    if location is None:
        return None
    return location.latitude, location.longitude


def get_friends(username: str) -> List[Friend]:
    resp = make_request(f"https://api.twitter.com/2/users/{get_user_id(username)}/following?"
                        f"user.fields=location,name,username")
    return [Friend(*get_coordinates(user["location"]), user["name"], user["username"])
            for user in resp["data"] if "location" in user]
