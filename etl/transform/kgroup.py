'''parse k group receipts'''

import json

from .common import Chain, Receipt, ParsingResult, Store


def transform(s3obj) -> ParsingResult:
    '''Transform an S3 ObjectSummary. Perhaps due a renaming and a typehint.'''

    data = json.load(s3obj.get()['Body'])

    receipt = Receipt(
        id=data['id'],
        total=int(data['grandAmount'] * 100),
        reprint=data['receiptReprint'],
        datetime=data['transactionDateTime'],
    )

    store = Store(
        id=data['businessUnit']['id'],
        name=data['businessUnit']['name']
    )

    chainlessname = data['businessUnit']['chainlessName']
    chain_name = store.name.replace(chainlessname, '').strip()

    chain = Chain(
        id=data['businessUnit']['chainId'],
        name=chain_name
    )

    return ParsingResult(
        receipt=receipt,
        store=store,
        chain=chain,
        etag=s3obj.e_tag
    )
