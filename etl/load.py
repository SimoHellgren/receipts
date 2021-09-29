'''Load data into a destination'''

import os
import requests
from typing import Iterable

from dotenv import load_dotenv

from etl.transform.common import ParsingResult


load_dotenv()


class BaseURLSession(requests.Session):
    '''A BaseURLSession works exactly like a requests.Session, except that it
        prepends a baseurl into every url it requests
    '''
    def __init__(self, baseurl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baseurl = baseurl

    def request(self, method, url, *args, **kwargs):
        return super().request(method, self.baseurl + url, *args, **kwargs)


api = BaseURLSession(os.environ['API_URL'])

def load(data: Iterable[ParsingResult]):
    '''Load data throuhg API. To save some requests, first gets the unique chains, stores etc. in the data, so each 
       only gets sent once. In case there were conflicting data present, the last one gets sent (which would happen
       also if we made separate requests).

       Our information about paymentmethods and products is incomplete, so we can't use PUT for them. Thus we check
       for their existence first, and POST them if needed. Everything else can be PUT.

       The order of operations is significant, since there are FK dependencies as follows:
        chain > store
        [store, paymentmethod] > receipt
        [receipt, product] > lines
       
       In a heavier production setting, something like this could be fun to implement in Airflow, though here such 
       would likely be overkill.
    '''

    chains = {}
    stores = {}
    paymentmethods = {}
    products = {}
    # receipts and lines can just be lists
    receipts = []
    lines = []

    for d in data:
        chains[d.chain_id] = {'id': d.chain_id, 'name': d.chain_name}
        stores[d.store_id] = {'id': d.store_id, 'name': d.store_id, 'chain_id': d.chain_id}
        paymentmethods[d.receipt_paymentmethod] = {'id': d.receipt_paymentmethod, 'payer': None} 

        receipts.append({
                'id': d.receipt_id,
                'datetime': d.receipt_datetime,
                'paymentmethod_id': d.receipt_paymentmethod,
                'total': d.receipt_total,
                'reprint': d.receipt_reprint,
                'etag': d.etag,
                'store_id': d.store_id
            })

        for line in d.receipt_items:
            products[line.product] = {'id': line.product, 'name': None}
            lines.append({
                'receipt_id': d.receipt_id,
                'linenumber': line.line_num,
                'product_id': line.product,
                'amount': line.price
                })

    existing_paymentmethods = api.get('/paymentmethods').json()
    existing_products = api.get('/products').json()

    existing_paymentmethod_ids = {x['id'] for x in existing_paymentmethods}
    existing_product_ids = {x['id'] for x in existing_products}

    paymentmethods_to_post = {v['id']: v for k, v in paymentmethods.items() if k not in existing_paymentmethod_ids}
    products_to_post = {v['id']: v for k, v in products.items() if k not in existing_product_ids}


    for chain in chains.values():
        api.put(f"/chains/{chain['id']}", json=chain)

    for store in stores.values():
        api.put(f"/stores/{store['id']}", json=store)

    for paymentmethod in paymentmethods_to_post.values():
        api.post('/paymentmethods', json=paymentmethod)

    for product in products_to_post.values():
        api.post('/products', json=product)

    for receipt in receipts:
        api.put(f"/receipts/{receipt['id']}", json=receipt)
    
    for line in lines:
        api.put(f"/receipts/{line['receipt_id']}/lines/{line['linenumber']}", json=line)
