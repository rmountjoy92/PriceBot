import os
import requests
from datetime import datetime
from typing import List

FRED_SERIES = {
    "rent": {"seriesid": "CUUR0000SEHA", "title": "Rent"},
    "condos": {"seriesid": "CHXRCSA", "title": "Condo"},
    "homeowners insurance": {
        "seriesid": "PCU9241269241262",
        "title": "Homeowners Insurance",
    },
    "mortgage interest rate": {
        "seriesid": "MORTGAGE30US",
        "title": "Mortgage Interest Rate",
    },
    "household furnishings": {
        "seriesid": "CUSR0000SAH3",
        "title": "Household Furnishing",
    },
    "new vehicles": {"seriesid": "CUUR0000SETA01", "title": "New Vehicle"},
    "used cars": {"seriesid": "CUSR0000SETA02", "title": "Used Car"},
    "medical care": {"seriesid": "CPIMEDNS", "title": "Medical Care"},
    "movie tickets": {
        "seriesid": "CUSR0000SS62031",
        "title": "Movie, Theater & Concert Ticket",
        "subtext": "Consumer Price Index for All Urban Consumers: Admission to Movies, Theaters, and Concerts",
    },
    "tuition & childcare": {"seriesid": "CUSR0000SEEB", "title": "Tuition & Child Care"},
    "toys": {"seriesid": "CUSR0000SERE01", "title": "Toy"},
}


class FREDClient:
    url_base = "https://api.stlouisfed.org/fred/series/observations"

    def __init__(self):
        self.api_key = os.getenv("FRED_API_KEY")

    def make_request(self, series_ids: List[str], start_year: str, end_year: str):
        results = {}
        for series_id in series_ids:
            params = {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "observation_start": f"{start_year}-01-01",
                "observation_end": f"{end_year}-12-31",
            }
            try:
                response = requests.get(self.url_base, params=params)
                response.raise_for_status()
                results[series_id] = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {series_id}: {e}")
                results[series_id] = {"error": str(e)}

        return results

    def get_fred_prices_post(self, post: dict) -> str:
        # Fetch data for the specified product
        data = self.make_request(
            [post['Series ID']],
            f"{datetime.now().year - 1}",
            f"{datetime.now().year}",
        )

        # Extract observations for the series
        series_id = post['Series ID']
        observations = data[series_id].get("observations", [])

        if not observations:
            return f"Error: No data available for {post['Name']}."

        # Get the latest price (last observation)
        latest_observation = observations[-1]
        latest_price = float(latest_observation["value"])
        latest_date = latest_observation["date"]

        # Find the price from approximately 12 months ago
        # Assuming monthly data, try to find the observation 12 months prior
        target_date = f"{int(latest_date[:4]) - 1}-{latest_date[5:7]}-01"
        price_one_year_ago = None
        for obs in observations:
            if obs["date"].startswith(target_date[:7]):  # Match year and month
                price_one_year_ago = float(obs["value"])
                break

        # Fallback: If no exact match, use the observation 12 steps back (if available)
        if price_one_year_ago is None and len(observations) >= 12:
            price_one_year_ago = float(observations[-13]["value"])
        elif price_one_year_ago is None:
            return f"Error: Insufficient data for {post['Name']} to calculate year-over-year change."

        # Calculate percentage change
        price_change = ((latest_price - price_one_year_ago) / price_one_year_ago) * 100
        change_direction = "+" if price_change >= 0 else "-"
        percentage_change = abs(round(price_change, 2))
        emoji = "📈" if change_direction == "+" else "📉"

        price_string = ""
        if post['Type'] == 'Price':
            price_string = f"""The current price for {post['Name'].lower()} is: ${latest_price:0.2f}
            
12 months ago it was: ${price_one_year_ago:0.2f}
"""
        if post['Type'] == 'Percent':
            price_string = f"""The current percent for {post['Name'].lower()} is: {latest_price:0.2f}%
12 months ago it was: {price_one_year_ago:0.2f}%
"""
        if post['Type'] == 'Index':
            price_string = f"""The current index for {post['Name'].lower()} is: ${latest_price:0.2f}
12 months ago it was: ${price_one_year_ago:0.2f}
"""

        # Format the output string
        return f"""{emoji} The price of {post['Name'].lower()} is {"increasing" if change_direction == "+" else "decreasing"}! {emoji}

{price_string}
That's a {percentage_change}% {'increase' if change_direction == '+' else 'decrease'}!

* Source: {post['Series Name']} | Federal Reserve Bank of St. Louis
"""
