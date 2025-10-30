from datetime import datetime
import requests
import json

from typing import List


class BLSClient:
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    def make_request(self, series_ids: List[str], start_year: str, end_year: str):
        p = requests.post(
            self.url,
            data=json.dumps(
                {"seriesid": series_ids, "startyear": start_year, "endyear": end_year}
            ),
            headers={"Content-type": "application/json"},
        )
        return json.loads(p.text)

    def get_bls_prices_post(self, post: dict) -> str:
        data = self.make_request(
            [post['Series ID']],
            f"{datetime.now().year - 1}",
            f"{datetime.now().year}",
        )
        latest_price = float(data["Results"]["series"][0]["data"][0]["value"])
        price_one_year_ago = float(data["Results"]["series"][0]["data"][12]["value"])

        price_change = ((latest_price - price_one_year_ago) / price_one_year_ago) * 100
        change_direction = "+" if price_change >= 0 else "-"
        percentage_change = abs(round(price_change, 2))
        emoji = "📈" if change_direction == "+" else "📉"

        return f"""{emoji} The price of {post['Name'].lower()} is {"increasing" if change_direction == "+" else "decreasing"}! {emoji}

The current price of {post['Name'].lower()} is: ${latest_price:0.2f}
The price of {post['Name'].lower()} 12 months ago was: ${price_one_year_ago:0.2f}

That's a {percentage_change}% {'increase' if change_direction == '+' else 'decrease'}!

* Source: {post['Series Name']} | U.S. Bureau of Labor Statistics
"""
