from sqlalchemy.orm import Session

from meirin.db import Session

from meirin.db.metapolicy import MetaPolicy
from meirin.db.policy import Policy

"""
subject:
    role: robot | ...

object:
    domain: "mao"
    type: "robotapi" | ...
"""

with Session() as session:
    mp = MetaPolicy(
        name="MaoMao API",
        match="object.domain == \"mao\"",
        mode="deny-overrides"
    )

    session.add(mp)
    session.commit()
    session.refresh(mp)

    p1 = Policy(
        name="default",
        group=mp.id,
        match="true",
        effect="permit"
    )

    p2 = Policy(
        name="Robot policy",
        group=mp.id,
        match="subject.role != \"robot\" && object.type == \"robotapi\"",
        effect="deny"
    )

    session.add(p1)
    session.add(p2)

    session.commit()
