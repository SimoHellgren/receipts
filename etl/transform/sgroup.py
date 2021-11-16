'''parse s group receipts'''
import json

from .common import Chain, Receipt, ParsingResult

def transform(s3obj) -> ParsingResult:
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])
    
    receipt = Receipt(
        id=data['eReceiptId'],
        total=int(data['transaction']['totalAmount'] * 100),
        reprint=data['receiptDetails']['eReceiptReprintData'],
        datetime=data['transaction']['transactionTimestamp'],
    )
    
    store_id = data['store']['storeId']
    store_name = data['store']['placeOfBusinessName']

    chain = Chain(
        id=data['chain']['chainCode'],
        name=data['chain']['chainName']
    )    

    return ParsingResult(
        receipt=receipt,
        store_id=store_id,
        store_name=store_name,
        chain=chain,
        etag=s3obj.e_tag
    )
