from os import getenv

# Price

# The minimum rent you want to pay per month.
MIN_PRICE = 0

# The maximum rent you want to pay per month.
MAX_PRICE = 3000

# The minimum and maximum number of bedrooms you want.
MIN_BEDROOMS = 2
MAX_BEDROOMS = 2

# Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'slo'

# POI preferences

# The farthest you want to live from a POI stop.
MAX_POI_DIST = 4  # Miles

# POI  you want to check against.  Every coordinate here will be checked against each listing,
# and the closest POI name will be added to the result and posted into Slack.
POI_LOCATIONS = {
    "Cal Poly": [35.303221, -120.663078]
}

# Search type preferences

# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
CRAIGSLIST_HOUSING_SECTION = 'apa'

# System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 20 * 60  # 20 minutes

# Which slack channel to post the listings into.
SLACK_CHANNEL = "#housing"

# Which slack username to use to post
SLACK_USER = "housing-bot"

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = getenv('SLACK_TOKEN', "")

# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass
