import os
import requests
import cloudscraper
from atproto import Client
from atproto_client.models.app.bsky.embed.external import External, Main
from bs4 import BeautifulSoup


class BlueskyClient:
    def __init__(self):
        self.username = os.getenv("BLUESKY_USERNAME")
        self.password = os.getenv("BLUESKY_PASSWORD")
        self.client = Client("https://bsky.social")
        self.client.login(self.username, self.password)

    def post(self, text: str, article_url: str = None) -> None:
        if article_url:
            self.client.post(text, embed=self.get_article_embed(article_url))
        else:
            self.client.post(text)

    def get_article_embed(self, article_url):
        title = ""
        description = ""
        img_blob = None

        scraper = cloudscraper.create_scraper()
        resp = scraper.get(article_url)


        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("meta", property="og:title")
        if title_tag:
            title = title_tag["content"]

        description_tag = soup.find("meta", property="og:description")
        if description_tag:
            description = description_tag["content"]

        image_tag = soup.find("meta", property="og:image")
        if image_tag:
            img_url = image_tag["content"]
            with scraper.get(img_url, stream=True, timeout=15) as resp:
                blob = b''.join(chunk for chunk in resp.iter_content(chunk_size=8192))
            img_blob = self.client.upload_blob(blob)
            img_blob = img_blob.blob

        return Main(external=External(uri=article_url, description=description, title=title, thumb=img_blob))

