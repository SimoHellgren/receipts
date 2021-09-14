'''Load data into a destination'''

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv

from models import Chain, Store, Receipt, Paymentmethod, Product, Receiptline


def load(data):
    load_dotenv()
    engine = create_engine(os.environ['DB_URI'])

    Session = sessionmaker(bind=engine)

    with Session() as sqlsession: # namings should be improved when separating load to own module
        for d, etag in data:
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
