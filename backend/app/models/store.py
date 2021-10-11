from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Text

from backend.app.db.base_class import Base


class Store(Base):
    __tablename__ = 'store'

    id = Column(Text, primary_key=True)
    name = Column(Text)
    chain_id = Column(Text, ForeignKey('chain.id'))
