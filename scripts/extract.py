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

from transform import kgroup, sgroup

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

dt = datetime(2021,9,14, tzinfo=timezone.utc)

with engine.connect() as conn:
    for d, etag in data_for_day(dt):
        
        # upsert chain
        conn.execute(
            '''insert into chain(id, name) values (%s, %s)
                on conflict on constraint chain_pkey do nothing
            ''',
            (d['chainid'], d['chainname'])
        )

        # upsert store
        conn.execute(
            '''insert into store(id, name, chain_id) values (%s, %s, %s)
                on conflict on constraint store_pkey do nothing
            ''',
            (d['storeid'], d['storename'], d['chainid'])
        )

        # upsert paymentmethod
        conn.execute(
            '''insert into paymentmethod(id) values (%s)
                on conflict on constraint paymentmethod_pkey do nothing
            ''',
            (d['paymentmethod'], )
        )

        # upsert receipt
        conn.execute(
            '''insert into receipt(id, reprint, total, etag) values (%s, %s, %s,%s)
                on conflict on constraint receipt_pkey do nothing
            ''', 
                (d['receiptid'], d['reprint'], d['total'], etag)
        )

        # upsert receipt items and products
        for linenum, product_id, amount in d['items']:
            conn.execute(
                '''insert into product(id) values (%s)
                    on conflict on constraint product_pkey do nothing
                ''',
                (product_id, )
            )

            conn.execute(
                '''insert into receiptline(receipt_id, linenumber, datetime, store_id, product_id, paymentmethod_id, amount)
                    values (%s, %s, %s, %s, %s, %s, %s)
                    on conflict on constraint receiptline_pkey do nothing
                ''',
                (d['receiptid'], linenum, d['datetime'], d['storeid'], product_id, d['paymentmethod'], amount)
            )
