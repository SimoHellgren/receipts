'''parse s group receipts'''
import json

from .common import extract_payment_method, extract_items

def transform(s3obj):
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])
    
    receiptid = data['eReceiptId'] 

    storeid = data['store']['storeId']
    storename = data['store']['placeOfBusinessName']

    datetime = data['transaction']['transactionTimestamp']
    total = data['transaction']['totalAmount']

    reprint = data['receiptDetails']['eReceiptReprintData']
    
    chainid = data['chain']['chainCode']
    chainname = data['chain']['chainName']
    chainlessname = storename.replace(chainname, '').strip()

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