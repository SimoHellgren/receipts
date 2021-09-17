'''Load data into a destination'''

import os
from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv

from etl.transform.common import ParsingResult
from .models import Chain, Store, Receipt, Paymentmethod, Product, Receiptline


def load(data: Iterable[ParsingResult]):
    '''Should maybe do a "load one"? I guess it's mostly a choice of letting the DB handle deduplication or not.'''
    load_dotenv()
    engine = create_engine(os.environ['DB_URI'])

    Session = sessionmaker(bind=engine)

    with Session() as session:
        for d in data:
            chain_stmt = insert(Chain).values(id=d.chain_id, name=d.chain_name).on_conflict_do_nothing()
            store_stmt = insert(Store).values(id=d.store_id, name=d.store_name, chain_id=d.store_id).on_conflict_do_nothing()
            paymentmethod_stmt = insert(Paymentmethod).values(id=d.receipt_paymentmethod).on_conflict_do_nothing()
            receipt_stmt = insert(Receipt).values(
                id=d.receipt_id,
                reprint=d.receipt_reprint,
                total=d.receipt_total,
                etag=d.etag,
                datetime=d.receipt_datetime,
                store_id=d.store_id,
                paymentmethod_id=d.receipt_paymentmethod
            ).on_conflict_do_nothing()


            session.execute(chain_stmt)
            session.execute(store_stmt)
            session.execute(paymentmethod_stmt)
            session.execute(receipt_stmt)

            for item in d.receipt_items:
                product_stmt = insert(Product).values(id=item.product).on_conflict_do_nothing()
                receiptline_stmt = insert(Receiptline).values(
                    receipt_id=d.receipt_id,
                    linenumber=item.line_num,
                    datetime=d.receipt_datetime,
                    store_id=d.store_id,
                    product_id=item.product,
                    paymentmethod_id=d.receipt_paymentmethod,
                    amount=item.price
                ).on_conflict_do_nothing()

                session.execute(product_stmt)
                session.execute(receiptline_stmt)

        session.commit()
