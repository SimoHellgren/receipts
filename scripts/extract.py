'''extract data from s3 bucket and dump into a DB'''

import os
from itertools import chain, islice
from functools import partial
import json

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

# get and transform kdata
kdata = bucket.objects.filter(Prefix='kdata')

# first result is skipped (tail), as it's just the folder 'kdata'
transformed_kdata = map(
    kgroup.transform,
    (json.load(e.get()['Body']) for e in tail(kdata))
)

# get and transform sdata
sdata = bucket.objects.filter(Prefix='sdata')

# first result skipped (tail), as it's just the folder 'sdata'
transformed_sdata = map(
    sgroup.transform,
    (json.load(e.get()['Body']) for e in tail(sdata))
)


engine = create_engine(os.environ['DB_URI'])

with engine.connect() as conn:
    for d in chain(transformed_kdata, transformed_sdata):
        conn.execute(
            '''insert into receipt(id, reprint, total) values (%s, %s, %s)
                on conflict on constraint receipt_pkey do nothing
            ''', 
                (d['receiptid'], d['reprint'], d['total'])
        )

