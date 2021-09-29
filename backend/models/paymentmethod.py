from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Text

from backend.db.base_class import Base


class Paymentmethod(Base):
    __tablename__ = 'paymentmethod'

    id = Column(Text, primary_key=True)
    payer = Column(Text)
