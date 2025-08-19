import os
from atproto import Client


class BlueskyClient:
    def __init__(self):
        self.username = os.getenv("BLUESKY_USERNAME")
        self.password = os.getenv("BLUESKY_PASSWORD")
        self.client = Client("https://bsky.social")
        self.client.login(self.username, self.password)

    def post(self, text: str) -> None:
        self.client.post(text)