from dotenv import load_dotenv
from datetime import datetime

from airtable_client import AirtableClient
from bluesky_client import BlueskyClient
from bls_client import BLSClient
from fred_client import FREDClient


load_dotenv()


def main():
    airtable_client = AirtableClient()
    posts = airtable_client.get_posts_from_airtable()
    post = next((item for item in posts if item['Day'] == datetime.now().day), None)
    if not post:
        raise Exception("No post found")

    bluesky_client = BlueskyClient()

    if post["Source"] == "FRED":
        fred_client = FREDClient()
        bluesky_client.post(fred_client.get_fred_prices_post(post), article_url=post.get('article'))

    if post["Source"] == "BLS":
        bls_client = BLSClient()
        bluesky_client.post(bls_client.get_bls_prices_post(post), article_url=post.get('article'))


if __name__ == "__main__":
    main()
