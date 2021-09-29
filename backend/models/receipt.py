from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Numeric, Text

from backend.db.base_class import Base


class Receipt(Base):
    __tablename__ = 'receipt'

    id = Column(Text, primary_key=True)
    reprint = Column(Text)
    total = Column(Numeric)
    etag = Column(Text)
    datetime = Column(TIMESTAMP(timezone=True))
    store_id = Column(Text, ForeignKey('store.id'))
    paymentmethod_id = Column(Text, ForeignKey('paymentmethod.id'))
