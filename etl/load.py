'''Load data into a destination'''

import os
from typing import Iterable

from dotenv import load_dotenv
from etl.receipt_api import ReceiptAPI
from etl.models import ReceiptCreate, Receiptline

from etl.transform.common import ParsingResult


load_dotenv()

api = ReceiptAPI(os.environ['API_URL'])


def load(data: Iterable[ParsingResult]):
    '''Load data through API. To save some requests, first gets the unique chains, stores etc. in the data, so each 
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
        chains[d.chain.id] = {'id': d.chain.id, 'name': d.chain.name}
        stores[d.store.id] = {'id': d.store.id, 'name': d.store.name, 'chain_id': d.chain.id}
        paymentmethods[d.receipt.paymentmethod] = {'id': d.receipt.paymentmethod, 'payer': None} 

        receipt = d.receipt
        receipts.append(ReceiptCreate(
            id=receipt.id,
            datetime=receipt.datetime,
            paymentmethod_id=receipt.paymentmethod,
            total=receipt.total,
            reprint=receipt.reprint,
            etag=d.etag,
            store_id=d.store.id
            )
        )

        for line in receipt.items:
            products[line.product] = {'id': line.product, 'name': None}
            lines.append(Receiptline(
                receipt_id=receipt.id,
                linenumber=line.line_num,
                product_id=line.product,
                amount=line.price
                )
            )

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
        api.put_receipt(receipt)
    
    for line in lines:
        api.put_receiptline(line)
