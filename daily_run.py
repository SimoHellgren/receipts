'''run ETL-pipeline for a single day's data'''

from datetime import datetime, timezone
from itertools import chain

from etl.extract import extract_by_date
from etl.transform import kgroup, sgroup
from etl.load import load


def main(run_date: datetime):
    print('Fetching data for', run_date.date())

    # get data
    kdata = extract_by_date('kdata', run_date)
    sdata = extract_by_date('sdata', run_date)

    transformed_kdata = map(kgroup.transform, kdata)
    transformed_sdata = map(sgroup.transform, sdata)

    load(chain(transformed_kdata, transformed_sdata))

if __name__ == '__main__':
    import sys

    # parse date from argv if it exists, otherwise current date
    if len(sys.argv) > 1:
        RUN_DATE = datetime.strptime(sys.argv[1], '%Y-%m-%d').replace(tzinfo=timezone.utc)
    else:
        RUN_DATE = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    main(RUN_DATE)
