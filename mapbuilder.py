from typing import List

from twitter import Friend
from folium import Map, FeatureGroup, Marker, Icon


def build_map(friends: List[Friend]) -> Map:
    html_map = Map(zoom_start=5)
    points_fg = FeatureGroup(name="Friends")
    for friend in friends:
        points_fg.add_child(Marker(location=(friend.latitude, friend.longitude), popup=friend.username, icon=Icon()))
    html_map.add_child(points_fg)

    return html_map
