'''parse k group receipts'''

from .common import extract_payment_method, extract_items


def transform(data: dict):
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
        'items': items
    }