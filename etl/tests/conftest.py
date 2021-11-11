from datetime import datetime
import json

import pytest

from etl import models

@pytest.fixture(scope='session')
def api_schema():
    with open('etl/receipt_api_schema.json', 'rb') as f:
        return json.load(f)


@pytest.fixture
def test_data():
    return {
        'receipt': models.ReceiptCreate(
            id='receipt_id',
            datetime=datetime(2021, 1, 1, 0, 0, 0, 0),
            paymentmethod_id='CASH',
            total=1000,
            reprint='This is where a reprint would be',
            etag='kjdflgkjiugvökjbsöh',
            store_id='k-market'
        ),

        'receiptline': models.Receiptline(
            linenumber=1,
            product_id='test_product',
            amount=100,
            receipt_id = 'receipt_id'
        )
    }
