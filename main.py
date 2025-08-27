from dotenv import load_dotenv
from datetime import datetime

from bluesky_client import BlueskyClient
from bls_client import BLSClient
from fred_client import FREDClient


load_dotenv()


POST_SCHEDULE = {
    1: {"name": "eggs", "source": "bls"},
    2: {"name": "electricity", "source": "bls"},
    3: {"name": "chicken", "source": "bls"},
    4: {"name": "rice", "source": "bls"},
    5: {"name": "milk", "source": "bls"},
    6: {"name": "beef", "source": "bls"},
    7: {"name": "bacon", "source": "bls"},
    8: {"name": "gas", "source": "bls"},
    9: {"name": "bread", "source": "bls"},
    10: {"name": "bananas", "source": "bls"},
    11: {"name": "orange", "source": "bls"},
    12: {"name": "ice cream", "source": "bls"},
    13: {"name": "steak", "source": "bls"},
    14: {"name": "coffee", "source": "bls"},
    15: {"name": "potato chips", "source": "bls"},
    16: {"name": "yogurt", "source": "bls"},
    17: {"name": "gasoline", "source": "bls"},
    18: {"name": "fuel oil", "source": "bls"},
    19: {"name": "soft drinks", "source": "bls"},
    20: {"name": "butter", "source": "bls"},
    21: {"name": "rent", "source": "fred"},
    22: {"name": "condos", "source": "fred"},
    23: {"name": "homeowners insurance", "source": "fred"},
    24: {"name": "mortgage interest", "source": "fred"},
    25: {"name": "household furnishings", "source": "fred"},
    26: {"name": "new vehicles", "source": "fred"},
    27: {"name": "used cars", "source": "fred"},
    28: {"name": "medical care", "source": "fred"},
    29: {"name": "movie tickets", "source": "fred"},
    30: {"name": "tuition childcare", "source": "fred"},
    31: {"name": "toys", "source": "fred"},
}


def main():
    bluesky_client = BlueskyClient()

    current_day = datetime.now().day
    post = POST_SCHEDULE[current_day]

    if post["source"] == "fred":
        fred_client = FREDClient()
        bluesky_client.post(fred_client.get_fred_prices_post(post["name"]))

    if post["source"] == "bls":
        bls_client = BLSClient()
        bluesky_client.post(bls_client.get_bls_prices_post(post["name"]))


if __name__ == "__main__":
    main()
