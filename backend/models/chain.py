from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Text

from backend.db.base_class import Base


class Chain(Base):
    __tablename__ = 'chain'

    id = Column(Text, primary_key=True)
    name = Column(Text)
