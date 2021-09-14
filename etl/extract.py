'''extract data from s3 bucket'''

from itertools import islice
from functools import partial
from datetime import datetime, timedelta

import boto3
from dotenv import load_dotenv

# utils
drop = lambda n, it: islice(it, n, None)
tail = partial(drop, 1)



def extract_by_date(folder: str, dt: datetime):
    # secrets from environment
    load_dotenv()
    
    # s3 connection
    session = boto3.Session()
    s3 = session.resource('s3')

    bucket = s3.Bucket('receipts-raw')
    # get files, skipping the first result as it's just the folder itself
    data = tail(bucket.objects.filter(Prefix=folder))

    # filter to relevant date
    predicate = lambda x: dt <= x.last_modified < (dt + timedelta(days=1))
    modified_since = filter(predicate, data)

    return modified_since
