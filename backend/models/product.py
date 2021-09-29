from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Text

from backend.db.base_class import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Text, primary_key=True)
    name = Column(Text)
