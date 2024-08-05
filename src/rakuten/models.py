from typing import List, Dict
import datetime
import json

class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []

class Product:
    def __init__(
        self,
        mid: str,
        merchantname: str,
        linkid: str,
        createdon: str,
        sku: str,
        productname: str,
        category: Dict,
        price: Dict,
        saleprice: Dict,
        upccode: str,
        description: Dict,
        keywords: str,
        linkurl: str,
        imageurl: str
    ):
        # Make the fields consistent
        self.advertiser_id = mid
        self.advertiser_name = merchantname
        self.link_id = linkid
        self.created_on = datetime.datetime.strptime(createdon, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.sku = sku
        self.name = productname
        self.category = category
        self.price = price
        self.sale_price = saleprice
        self.upccode = upccode
        self.description = description
        self.keywords = keywords
        self.link_url = linkurl
        self.image_url = imageurl

        # Fix the price fields
    def __str__(self) -> str:
        as_dict = self.__dict__
        # Convert datetimes
        as_dict["created_on"] = self.created_on.strftime("%m/%d/%Y, %H:%M:%S")
        return json.dumps(as_dict, indent=2)

class Advertiser:
    def __init__(
        self,
        id: int,
        name: str,
        network: int = None,
        url: str = None,
        description: str = None,
        profiles: Dict = None,
        policies: Dict = None,
        features: Dict = None,
        contact: Dict = None,
        network_status: str = None
    ):
        self.id = id
        self.name = name
        self.url = url
        self.description = description
        self.profiles = profiles
        self.policies = policies
        self.features = features
        self.contact = contact
        self.network_status = network_status
        self.network = network

class Event:
    def __init__(
        self,
        etransaction_id: str,
        advertiser_id: str,
        sid: str,
        order_id: str,
        offer_id: str,
        sku_number: str,
        sale_amount: float,
        quantity: int,
        commissions: float,
        process_date: str,
        transaction_date: str,
        transaction_type: str,
        product_name: str,
        u1: str,
        currency: str,
        is_event: bool,
        commission_list_id: str
    ):
        self.etransaction_id = etransaction_id
        self.advertiser_id = advertiser_id
        self.sid = sid
        self.order_id = order_id
        self.offer_id = offer_id
        self.sku_number = sku_number
        self.sale_amount = sale_amount
        self.quantity = quantity
        self.commissions = commissions
        self.process_date = datetime.datetime.strptime(
            process_date.split(" (")[0],
            "%a %b %d %Y %H:%M:%S %Z%z"
        )
        self.transaction_date = datetime.datetime.strptime(
            transaction_date.split(" (")[0],
            "%a %b %d %Y %H:%M:%S %Z%z"
        )
        self.transaction_type = transaction_type
        self.product_name = product_name
        self.u1 = u1
        self.currency = currency
        self.is_event = is_event
        self.commission_list_id = commission_list_id

    def __str__(self) -> str:
        as_dict = self.__dict__
        # Convert datetimes
        as_dict["process_date"] = self.process_date.strftime("%m/%d/%Y, %H:%M:%S")
        as_dict["transaction_date"] = self.transaction_date.strftime("%m/%d/%Y, %H:%M:%S")
        return json.dumps(as_dict, indent=2)
    