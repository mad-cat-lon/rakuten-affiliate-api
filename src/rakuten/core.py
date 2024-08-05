from rakuten.rest_adapter import RestAdapter
from rakuten.models import Event, Advertiser, Product
import datetime
from typing import List, Literal

    
class Rakuten:
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
    
    def get_payments(
        self,
        report_type: Literal["all_history", "advertisers_history", "details"],
        security_token: str,
        network_id: int = None,
        payment_id: int = None,
        report_date_start: datetime.date = None,
        report_date_end: datetime.date = None,
        invoice_id: int = None,
        advertiser_id: int = None
    ):
        endpoint = "/advancedreports/1.0"
        if report_type == "all_history":
            #  bdate and edate are mandatory
            if not report_date_start or not report_date_end:
                raise ValueError("Payment history summary requires start date and end date")
            
        params = {
            "token": security_token
        }
        match report_type:
            case "all_history":
                params["reportid"] = 1
            case "advertisers_history":
                params["reportid"] = 2
            case "details":
                params["reportid"] = 3
        if report_date_start:
            params["bdate"] = report_date_start.strftime("%Y%m%d")
        if report_date_end:
            params["edate"] = report_date_end.strftime("%Y%m%d")
        if payment_id:
            params["payid"] = payment_id
        if network_id:
            params["nid"] = network_id
        if invoice_id:
            params["invoiceid"] = invoice_id
        if advertiser_id:
            params["mid"] = advertiser_id
        result = self.adapter.get(endpoint=endpoint, params=params, return_type="csv")
        return result

    def get_coupons(
        self,
        category_ids: List[int] = None,
        promotion_type_ids: List[int] = None,
        network_id: int = None,
        advertiser_id: int = None,
        num_results: int = None,
        page: int = None
    ):
        endpoint = "/coupon/1.0"
        params = {}
        if category_ids:
            params["category"] = "|".join([str(i) for i in category_ids])
        if promotion_type_ids:
            params["promotiontype"] = "|".join([str(i) for i in promotion_type_ids])
        if network_id:
            params["network"] = network_id
        if advertiser_id:
            params["mid"] = advertiser_id
        result = self.adapter.get(endpoint=endpoint, params=params, return_type="xml")
        return result.data
    
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
        https://developers.rakutenadvertising.com/documentation/en-CA/affiliate_apis#/Events/get_events_1_0_transactions
        """
        params = {
            "process_date_start": process_date_start.strftime("%Y-%m-%d %H:%M:%S"),
            "process_date_end": process_date_end.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_date_start": transaction_date_start.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_date_end": transaction_date_end.strftime("%Y-%m-%d %H:%M:%S")
        }
        endpoint = "/events/1.0/transactions"
        result = self.adapter.get(endpoint=endpoint, params=params)
        events = [Event(**event) for event in result.data]
        return events
    
    def search_advertisers_v1(self, advertiser_name: str) -> List[Advertiser]:
        """
        Find a list of all advertisers and advertiser MIDs given a search string
        https://developers.rakutenadvertising.com/documentation/en-CA/affiliate_apis#/Events/get_events_1_0_transactions
        """
        params = {
            "merchantname": advertiser_name
        }
        endpoint = "/advertisersearch/1.0"
        result = self.adapter.get(
            endpoint=endpoint,
            params=params,
            return_type="xml"
        ).data["result"]["midlist"]["merchant"]
        # Change "mid" to "id" and "merchantname" to "name"
        result = [{"id": res["mid"], "name": res["merchantname"]} for res in result]
        advertisers = [Advertiser(**advertiser) for advertiser in result]
        return advertisers

    def search_advertisers_v2(
        self,
        page: int = 0,
        limit: int = 10,
        ships_to: str = "US",
        deep_links: bool = True,
        network: int = 1
    ) -> List[Advertiser]:
        """
        Updated version of advertiser searchht API that
        tps://developers.rakutenadvertising.com/documentation/en-CA/affiliate_apis#/Advertisers/get_v2_advertisers
        """
        endpoint = "/v2/advertisers"
        params = {
            "page": page,
            "limit": limit,
            "ships_to": ships_to,
            "deep_links": deep_links,
            "network": network
        }
        result = self.adapter.get(
            endpoint=endpoint,
            params=params
        ).data["advertisers"]
        advertisers = [Advertiser(**advertiser) for advertiser in result]
        return advertisers

    def search_products(
        self,
        keyword: str = None,
        exact: str = None,
        one: str = None,
        cat: str = None,
        language: str = "en_US",
        max: int = 100,
        page_number: int = 1,
        advertiser_id: int = None,
        sort: str = None,
        sort_type: str = None
    ):
        """
        https://developers.rakutenadvertising.com/documentation/en-CA/affiliate_apis#/Events/get_events_1_0_transactions
        """
        endpoint = "/productsearch/1.0"
        params = {
            "keyword": keyword,
            "exact": exact,
            "one": one,
            "cat": cat,
            "language": language,
            "max": max,
            "pagenumber": page_number,
            "mid": advertiser_id,
            "sort": sort,
            "sorttype": sort_type

        }
        result = self.adapter.get(
            endpoint=endpoint,
            params=params,
            return_type="xml"
        ).data["result"]["item"]
        return [Product(**res) for res in result]
    
    def generate_deep_links(
        self,
        url: str,
        advertiser_id: int,
        u1: str = None
    ):
        """
        Generates deep links with partner advertiser's product links
        https://developers.rakutenadvertising.com/documentation/en-US/affiliate_apis#/Deep%20Link/post_v1_links_deep_links
        """
        endpoint = "/v1/links/deep_links"
        body = {
            "url": url,
            "advertiser_id": advertiser_id,
        }
        if u1:
            body["u1"] = u1
        result = self.adapter.post(
            endpoint=endpoint,
            data=body,
            is_json=True
        ).data["advertiser"]
        return result["deep_link"]
    
