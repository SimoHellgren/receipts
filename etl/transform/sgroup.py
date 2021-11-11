'''parse s group receipts'''
import json

from .common import extract_payment_method, extract_items, ParsingResult

def transform(s3obj) -> ParsingResult:
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])
    
    receipt_id = data['eReceiptId'] 
    total = int(data['transaction']['totalAmount'] * 100)
    reprint = data['receiptDetails']['eReceiptReprintData']
    datetime = data['transaction']['transactionTimestamp']
    
    paymentmethod = extract_payment_method(reprint)
    items = extract_items(reprint)

    store_id = data['store']['storeId']
    store_name = data['store']['placeOfBusinessName']
    
    chain_id = data['chain']['chainCode']
    chain_name = data['chain']['chainName']

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
