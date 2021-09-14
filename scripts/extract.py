'''extract data from s3 bucket and dump into a DB'''

import os
from itertools import islice
from functools import partial
from datetime import datetime, timedelta, timezone
import json
from typing import Callable

import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from transform import kgroup, sgroup
from models import Chain, Store, Receipt, Paymentmethod, Product, Receiptline

load_dotenv()

# utils
drop = lambda n, it: islice(it, n, None)
tail = partial(drop, 1)

# s3 connection
# secrets from environment
session = boto3.Session()
s3 = session.resource('s3')

bucket = s3.Bucket('receipts-raw')


def get_and_transform_for_date(folder: str, transformer: Callable, dt: datetime):
    # get files, skipping the first result as it's just the folder itself
    data = tail(bucket.objects.filter(Prefix=folder))

    # filter to relevant date
    predicate = lambda x: dt <= x.last_modified < (dt + timedelta(days=1))
    modified_since = filter(predicate, data)

    # apply transformation, yield the result and ETag for the resource
    for obj in modified_since:
        contents = obj.get()['Body']
        transformed = transformer(json.load(contents))
        yield transformed, obj.e_tag


def data_for_day(dt: datetime):
    '''I don't like the name of this function'''
    yield from get_and_transform_for_date('kdata', kgroup.transform, dt)
    yield from get_and_transform_for_date('sdata', sgroup.transform, dt)


engine = create_engine(os.environ['DB_URI'])

Session = sessionmaker(bind=engine)

dt = datetime(2021,9,14, tzinfo=timezone.utc)

with Session() as sqlsession: # namings should be improved when separating load to own module
    for d, etag in data_for_day(dt):
        chain_stmt = insert(Chain).values(id=d['chainid'], name=d['chainname']).on_conflict_do_nothing()
        store_stmt = insert(Store).values(id=d['storeid'], name=d['storename'], chain_id=d['chainid']).on_conflict_do_nothing()
        paymentmethod_stmt = insert(Paymentmethod).values(id=d['paymentmethod']).on_conflict_do_nothing()
        receipt_stmt = insert(Receipt).values(id=d['receiptid'], reprint=d['reprint'], total=d['total'], etag=etag).on_conflict_do_nothing()


        sqlsession.execute(chain_stmt)
        sqlsession.execute(store_stmt)
        sqlsession.execute(paymentmethod_stmt)
        sqlsession.execute(receipt_stmt)

        for linenum, product_id, amount in d['items']:
            product_stmt = insert(Product).values(id=product_id).on_conflict_do_nothing()
            receiptline_stmt = insert(Receiptline).values(
                receipt_id=d['receiptid'],
                linenumber=linenum,
                datetime=d['datetime'],
                store_id=d['storeid'],
                product_id=product_id,
                paymentmethod_id=d['paymentmethod'],
                amount=amount
            ).on_conflict_do_nothing()

            sqlsession.execute(product_stmt)
            sqlsession.execute(receiptline_stmt)

    sqlsession.commit()
