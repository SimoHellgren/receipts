from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, Numeric, Text


Base = declarative_base()

class Chain(Base):
    __tablename__ = 'chain'

    id = Column(Text, primary_key=True)
    name = Column(Text)


class Store(Base):
    __tablename__ = 'store'

    id = Column(Text, primary_key=True)
    name = Column(Text)
    chain_id = Column(Text, ForeignKey('chain.id'))


class Paymentmethod(Base):
    __tablename__ = 'paymentmethod'

    id = Column(Text, primary_key=True)
    payer = Column(Text)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Text, primary_key=True)
    name = Column(Text)


class Receipt(Base):
    __tablename__ = 'receipt'

    id = Column(Text, primary_key=True)
    reprint = Column(Text)
    total = Column(Numeric)
    etag = Column(Text)
    datetime = Column(TIMESTAMP(timezone=True))
    store_id = Column(Text, ForeignKey('store.id'))
    paymentmethod_id = Column(Text, ForeignKey('paymentmethod.id'))


class Receiptline(Base):
    __tablename__ = 'receiptline'

    receipt_id = Column(Text, ForeignKey('receipt.id'), primary_key=True)
    linenumber = Column(Integer, primary_key=True)
    datetime = Column(TIMESTAMP(timezone=True))
    store_id = Column(Text, ForeignKey('store.id'))
    product_id = Column(Text, ForeignKey('product.id'))
    paymentmethod_id = Column(Text, ForeignKey('paymentmethod.id'))
    amount = Column(Numeric)
