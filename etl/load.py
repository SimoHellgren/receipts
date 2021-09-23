'''Load data into a destination'''

import os
import requests
from typing import Iterable

from dotenv import load_dotenv

from etl.transform.common import ParsingResult

load_dotenv()

def post(endpoint: str, data: dict):
    baseurl = os.environ['API_URL']
    return requests.post(baseurl+endpoint, json=data)


def load(data: Iterable[ParsingResult]):
    '''Most of these should probably be PUT'''
    for d in data:
        chain = post('/chains', {'id': d.chain_id, 'name': d.chain_name})
        store = post('/stores', {'id': d.store_id, 'name': d.store_id, 'chain': d.chain_id})
        paymentmethod = post('/paymentmethods', {'id': d.receipt_paymentmethod, 'payer': None})
        receipt = post(
            '/receipts',
            {
                'id': d.receipt_id,
                'datetime': d.receipt_datetime,
                'paymentmethod_id': d.receipt_paymentmethod,
                'total': d.receipt_total,
                'reprint': d.receipt_reprint,
                'etag': d.etag,
                'store_id': d.store_id
            }
        )

        lines = []
        for line in d.receipt_items:
            post('/products', {'id': line.product})
            lines.append({'linenumber': line.line_num, 'product_id': line.product, 'amount': line.price})

        items = post(f'/receipts/{d.receipt_id}/lines', lines)
