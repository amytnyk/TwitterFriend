import json
import os.path
from typing import Optional, Dict, Tuple
from geopy import Nominatim
from geopy.exc import GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter


def load_cache() -> Dict:
    if os.path.exists('geocache'):
        with open('geocache', 'r', encoding='utf-8') as file:
            return json.loads(file.read())
    return {}


def save_cache():
    with open('geocache', 'w', encoding='utf-8') as file:
        return file.write(json.dumps(cache))


def fetch_coordinates(location: str) -> Optional[Tuple[float, float]]:
    location = geocode(location)
    try:
        if location is None:
            return None
        return location.latitude, location.longitude
    except GeocoderUnavailable:
        return None


def get_coordinates(location: str) -> Optional[Tuple[float, float]]:
    if location not in cache:
        cache[location] = fetch_coordinates(location)
        save_cache()
    return cache[location]


geolocator = Nominatim(user_agent="TwitterFriend")
geocode = RateLimiter(geolocator.geocode)
cache = load_cache()
