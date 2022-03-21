from __future__ import annotations
from settings import SLACK_CHANNEL, SLACK_USER, POI_LOCATIONS, MAX_POI_DIST
from slack_sdk.web.client import WebClient
from math import radians, sin, cos, asin, sqrt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scraper import Listing


def coord_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Finds the distance between two pairs of latitude and longitude.
    :param lat1: Point 1 latitude.
    :param lon1: Point 1 longitude.
    :param lat2: Point two latitude.
    :param lon2: Point two longitude.
    :return: Mile distance.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * \
        cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    mi = 6367 * 0.621371 * c
    return mi


def post_listing_to_slack(slack_client: WebClient, listing: Listing):
    """
    Posts the listing to slack.
    :param slack_client: A slack client.
    :param listing: A record of the listing.
    """
    if listing.near_poi:
        desc = "@channel {0} | {1} | {2} mi from {3}".format(
            listing.name, listing.link, str(round(listing.poi_dist, 2)), listing.poi_name)

        slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=desc,
                                      username=SLACK_USER, icon_emoji=':robot_face:', link_names=True)


def find_points_of_interest(geotag: tuple[float, float]):
    """
    Find points of interest near a result.
    :param geotag: The geotag field of a Craigslist result.
    :return: A dictionary containing annotations.
    """
    min_dist = None
    near_poi = False
    poi_dist = "N/A"
    poi = ""

    # Check to see if the listing is near any transit stations.
    for station, coords in POI_LOCATIONS.items():
        dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])
        if (min_dist is None or dist < min_dist) and dist < MAX_POI_DIST:
            poi = station
            near_poi = True

        if (min_dist is None or dist < min_dist):
            poi_dist = dist

    return {
        "near_poi": near_poi,
        "poi_dist": poi_dist,
        "poi_name": poi
    }
