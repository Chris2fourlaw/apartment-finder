from settings import CRAIGSLIST_SITE, CRAIGSLIST_HOUSING_SECTION, MAX_BEDROOMS, MIN_BEDROOMS, MAX_PRICE, MIN_PRICE, SLACK_TOKEN
from time import ctime
from craigslist import CraigslistHousing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import find_points_of_interest, post_listing_to_slack
from slack_sdk.web.client import WebClient

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()


class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    near_poi = Column(Boolean)
    poi_name = Column(String)
    poi_dist = Column(Float)
    cl_id = Column(Integer, unique=True)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def scrape_housing():
    """
    Scrapes craigslist, and finds the latest listings.ß
    :return: A list of results.
    """
    cl_h = CraigslistHousing(
        site=CRAIGSLIST_SITE,
        category=CRAIGSLIST_HOUSING_SECTION,
        filters={
            'max_price': MAX_PRICE,
            'min_price': MIN_PRICE,
            'min_bedrooms': MIN_BEDROOMS,
            'max_bedrooms': MAX_BEDROOMS,
        }
    )

    listings: list[Listing] = []
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing: Listing = session.query(
            Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            lat = 0.0
            lon = 0.0
            if result["geotag"] is not None:
                # Assign the coordinates.
                lat: float = result["geotag"][0]
                lon: float = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest((lat, lon))
                result.update(geo_data)

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                name=result["name"],
                price=price,
                near_poi=result["near_poi"],
                poi_name=result["poi_name"],
                poi_dist=result["poi_dist"],
                cl_id=result["id"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            listings.append(listing)

    return listings


def do_scrape():
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    slack_client = WebClient(SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = scrape_housing()

    print("{}: Got {} results".format(ctime(), len(all_results)))

    # Post each result to slack.
    for listing in all_results:
        post_listing_to_slack(slack_client, listing)
