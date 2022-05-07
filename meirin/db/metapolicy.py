from sqlalchemy import Column, Sequence
from sqlalchemy import Integer, String, Text
from meirin.db.base_class import Base

class MetaPolicy(Base):
    __tablename__ = 'metapolicy'

    # helper

    metapolicy_id_seq = Sequence('metapolicy_id_seq', metadata=Base.metadata)

    # columns

    id   = Column(Integer, metapolicy_id_seq, server_default=metapolicy_id_seq.next_value(), primary_key = True)
    name = Column(String(64))

    match = Column(Text)
    mode  = Column(String(64))

    # TODO: index https://docs.sqlalchemy.org/en/14/orm/extensions/indexable.html

    def __repr__(self):
        return f"MetaPolicy(id={self.id!r}, name={self.name!r})"
