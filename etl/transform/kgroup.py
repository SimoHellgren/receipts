'''parse k group receipts'''

import json

from .common import Receipt, ParsingResult


def transform(s3obj) -> ParsingResult:
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])

    receipt = Receipt(
        id = data['id'],
        total = int(data['grandAmount'] * 100),
        reprint = data['receiptReprint'],
        datetime = data['transactionDateTime'],
    )

    store_id = data['businessUnit']['id']
    store_name = data['businessUnit']['name']

    chain_id = data['businessUnit']['chainId']
    chainlessname = data['businessUnit']['chainlessName']
    chain_name = store_name.replace(chainlessname, '').strip()

    return ParsingResult(
        receipt=receipt,
        store_id=store_id,
        store_name=store_name,
        chain_id=chain_id,
        chain_name=chain_name,
        etag=s3obj.e_tag
    )
