from datetime import datetime
import requests
import json

from typing import List


BLS_SERIES = {
    "eggs": {"seriesid": "APU0000708111", "title": "Egg"},
    "electricity": {"seriesid": "APU000072610", "title": "Electricity"},
    "chicken": {"seriesid": "APU0000706111", "title": "Chicken"},
    "rice": {"seriesid": "APU0000701312", "title": "Rice"},
    "milk": {"seriesid": "APU0000709112", "title": "Milk"},
    "beef": {"seriesid": "APU0000703112", "title": "Beef"},
    "bacon": {"seriesid": "APU0000704111", "title": "Bacon"},
    "gas": {"seriesid": "APU000074714", "title": "Gas"},
    "bread": {"seriesid": "APU0000702111", "title": "Bread"},
    "bananas": {"seriesid": "APU0000711211", "title": "Banana"},
    "orange": {"seriesid": "APU0000711311", "title": "Orange"},
    "ice cream": {"seriesid": "APU0000710411", "title": "Ice Cream"},
    "steak": {"seriesid": "APU0000703613", "title": "Steak"},
    "coffee": {"seriesid": "APU0000717311", "title": "Coffee"},
    "potato chips": {"seriesid": "APU0000718311", "title": "Potato Chip"},
    "yogurt": {"seriesid": "APU0000FJ4101", "title": "Yogurt"},
    "gasoline": {"seriesid": "APU00007471A", "title": "Gasoline"},
    "fuel oil": {"seriesid": "APU000072511", "title": "Fuel Oil"},
    "soft drinks": {"seriesid": "APU0000FN1101", "title": "Soft Drink"},
    "butter": {"seriesid": "APU0000FS1101", "title": "Butter"},
}


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

    def get_bls_prices_post(self, product_name: str) -> str:
        data = self.make_request(
            [BLS_SERIES[product_name]["seriesid"]],
            f"{datetime.now().year - 1}",
            f"{datetime.now().year}",
        )
        latest_price = float(data["Results"]["series"][0]["data"][0]["value"])
        price_one_year_ago = float(data["Results"]["series"][0]["data"][12]["value"])

        price_change = ((latest_price - price_one_year_ago) / price_one_year_ago) * 100
        change_direction = "+" if price_change >= 0 else "-"
        percentage_change = abs(round(price_change, 2))
        emoji = "📈" if change_direction == "+" else "📉"

        return f"""{emoji} {BLS_SERIES[product_name]['title']} prices are {"increasing" if change_direction == "+" else "decreasing"}! {emoji}

The current price of {product_name} is: ${latest_price:0.2f}
The price of {product_name} 12 months ago was: ${price_one_year_ago:0.2f}

That's a {percentage_change}% {'increase' if change_direction == '+' else 'decrease'}!

* Source: U.S. Bureau of Labor Statistics
"""
