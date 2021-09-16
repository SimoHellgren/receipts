'''parse k group receipts'''

import json

from .common import extract_payment_method, extract_items


def transform(s3obj):
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])

    receiptid = data['id']

    storeid = data['businessUnit']['id']
    storename = data['businessUnit']['name']

    datetime = data['transactionDateTime']
    total = data['grandAmount']
    reprint = data['receiptReprint']
    
    chainid = data['businessUnit']['chainId']
    chainlessname = data['businessUnit']['chainlessName']
    chainname = storename.replace(chainlessname, '').strip()

    paymentmethod = extract_payment_method(reprint)

    items = extract_items(reprint)

    return {
        'receiptid': receiptid,
        'storeid': storeid,
        'storename': storename,
        'datetime': datetime,
        'total': total,
        'reprint': reprint,
        'chainid': chainid,
        'chainname': chainname,
        'paymentmethod': paymentmethod,
        'items': items,
        'etag': s3obj.e_tag
    }