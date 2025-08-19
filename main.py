from dotenv import load_dotenv

from bluesky_client import BlueskyClient
from bls_client import BLSClient


load_dotenv()


def main():
    bluesky_client = BlueskyClient()
    bls_client = BLSClient()

    bluesky_client.post(bls_client.get_egg_prices_post())



if __name__ == '__main__':
    main()