from rakwrap.rest_adapter import RestAdapter
from rakwrap.models import Result, Event
import datetime
from typing import List

class Rakwrap:
    def __init__(self, client_id: str, client_secret: str, account_id: int):
        self.base_url = "https://api.linksynergy.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        self.adapter = RestAdapter(
            self.base_url,
            client_id=client_id,
            client_secret=client_secret,
            account_id=account_id
        )

    def auth(self):
        return self.adapter.get_token()
    
    def get_events(
        self,
        process_date_start: datetime.datetime,
        process_date_end: datetime.datetime,
        transaction_date_start: datetime.datetime,
        transaction_date_end: datetime.datetime,
        limit: int = 100,
        page: int = 1,
        currency: str = None,
        transaction_type: str = None
    ) -> List[Event]:
        """
        Retrieves transaction confirmations completed on a partner advertiser's website
        """
        params = {
            "process_date_start": process_date_start.strftime("%Y-%m-%d %H:%M:%S"),
            "process_date_end": process_date_end.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_date_start": transaction_date_start.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_date_end": transaction_date_end.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(params)
        endpoint = "/events/1.0/transactions"
        result = self.adapter.get(endpoint=endpoint, params=params)
        events = [Event(**event) for event in result.data]
        return events