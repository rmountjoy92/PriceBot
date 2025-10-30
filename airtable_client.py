import os
from pyairtable import Table


class AirtableClient(object):
    def __init__(self):
        self.api_key = os.getenv("AIRTABLE_KEY")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")

    def get_posts_from_airtable(self):
        table = Table(
            api_key=self.api_key,
            base_id=self.base_id,
            table_name='Posts'
        )

        return [record['fields'] for record in table.all()]
