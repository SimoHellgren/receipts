from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Integer, Text

from backend.app.db.base_class import Base


class Receiptline(Base):
    __tablename__ = 'receiptline'

    receipt_id = Column(Text, ForeignKey('receipt.id'), primary_key=True)
    linenumber = Column(Integer, primary_key=True)
    product_id = Column(Text, ForeignKey('product.id'))
    amount = Column(Integer)
