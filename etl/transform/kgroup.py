'''parse k group receipts'''

import json

from .common import extract_payment_method, extract_items, ParsingResult


def transform(s3obj) -> ParsingResult:
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])
    receipt_id = data['id']
    total = int(data['grandAmount'] * 100)
    reprint = data['receiptReprint']
    datetime = data['transactionDateTime']

    paymentmethod = extract_payment_method(reprint)
    items = extract_items(reprint)
    store_id = data['businessUnit']['id']
    store_name = data['businessUnit']['name']

    chain_id = data['businessUnit']['chainId']
    chainlessname = data['businessUnit']['chainlessName']
    chain_name = store_name.replace(chainlessname, '').strip()

    return ParsingResult(
        receipt_id=receipt_id,
        receipt_reprint=reprint,
        receipt_total=total,
        receipt_datetime=datetime,
        receipt_paymentmethod=paymentmethod,
        receipt_items=items,
        store_id=store_id,
        store_name=store_name,
        chain_id=chain_id,
        chain_name=chain_name,
        etag=s3obj.e_tag
    )
