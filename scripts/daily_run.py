'''run ETL-pipeline for a single day's data'''

from datetime import datetime, timezone
from itertools import chain
import json

from extract import extract_by_date
from transform import kgroup, sgroup
from load import load


def transform(data, transformer):
    '''Not sure if this should be in this module.

        Also, this is coupled to S3, so maybe there shoud be clear contracts / interfaces in the pipeline
    '''
    # apply transformation, yield the result and ETag for the resource
    for obj in data:
        contents = obj.get()['Body']
        transformed = transformer(json.load(contents))
        yield transformed, obj.e_tag




if __name__ == '__main__':
    
    RUN_DATE = datetime(2021, 9, 13, tzinfo=timezone.utc)

    # get data
    kdata = extract_by_date('kdata', RUN_DATE)
    sdata = extract_by_date('sdata', RUN_DATE)

    transformed_kdata = transform(kdata, kgroup.transform)
    transformed_sdata = transform(sdata, sgroup.transform)

    load(chain(transformed_kdata, transformed_sdata))