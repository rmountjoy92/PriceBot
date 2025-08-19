from datetime import datetime
import requests
import json

from typing import List


class BLSClient:
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

    def make_request(self, series_ids: List[str], start_year: str, end_year: str):
        p = requests.post(
            self.url,
            data=json.dumps({"seriesid": series_ids, "startyear": start_year, "endyear": end_year}),
            headers={'Content-type': 'application/json'}
        )
        return json.loads(p.text)

    def get_egg_prices_post(self) -> str:
        data = self.make_request(['APU0000708111'], f"{datetime.now().year - 1}", f"{datetime.now().year}")
        latest_egg_price = float(data['Results']['series'][0]['data'][0]['value'])
        egg_price_one_year_ago = float(data['Results']['series'][0]['data'][12]['value'])

        price_change = ((latest_egg_price - egg_price_one_year_ago) / egg_price_one_year_ago) * 100
        change_direction = "increase" if price_change >= 0 else "decrease"
        percentage_change = abs(round(price_change, 2))

        return f"""🥚 Egg price update! 🥚
The current price of eggs is: ${latest_egg_price:0.2f}
The price of eggs 12 months ago was: ${egg_price_one_year_ago:0.2f}

That's a {percentage_change}% {change_direction}!

* Source: U.S. Bureau of Labor Statistics
Eggs, grade A, large, per doz. in U.S. city average, average price, not seasonally adjusted 
"""