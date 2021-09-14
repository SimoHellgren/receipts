'''extract data from s3 bucket'''

from itertools import islice
from functools import partial
from datetime import datetime, timedelta

import boto3
from dotenv import load_dotenv

# utils
drop = lambda n, it: islice(it, n, None)
tail = partial(drop, 1)

def extract_datetime_range(folder: str, start_dt: datetime, end_dt: datetime):
    '''Extract data from a S3 bucket / logical folder if modified time is in [start_dt, end_dt)'''
    # secrets from environment
    load_dotenv()
    
    # s3 connection
    session = boto3.Session()
    s3 = session.resource('s3')

    bucket = s3.Bucket('receipts-raw')
    # get files, skipping the first result as it's just the folder itself
    data = tail(bucket.objects.filter(Prefix=folder))

    # filter to relevant date
    predicate = lambda x: start_dt <= x.last_modified < end_dt
    modified_since = filter(predicate, data)

    return modified_since


def extract_by_date(folder: str, start_dt: datetime):
    '''special case of `extract_datetime_range` where end_dt is one day from start_dt'''
    end_dt = start_dt + timedelta(days=1)
    return extract_datetime_range(folder, start_dt, end_dt)
