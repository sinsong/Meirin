from sqlalchemy import Column, ForeignKey, Sequence
from sqlalchemy import Integer, String, Text
from meirin.db.base_class import Base

class Policy(Base):
    __tablename__ = 'policy'

    # helper

    policy_id_seq = Sequence('policy_id_seq', metadata=Base.metadata)

    # columns

    id    = Column(Integer, policy_id_seq, server_default=policy_id_seq.next_value(), primary_key = True)
    name  = Column(String(64))
    group = Column(Integer, ForeignKey('metapolicy.id'))

    match  = Column(Text)
    effect = Column(String(64))

    def __repr__(self):
        return f"Policy(id={self.id!r}, name={self.name!r})"
