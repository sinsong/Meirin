from typing import Optional

from pydantic import BaseModel

class PolicyInput(BaseModel):
    name   :str
    group  :int
    match  :str
    effect :str

class PolicySchema(BaseModel):
    """策略
    """
    id :Optional[int]

    name   :str
    group  :int
    match  :str
    effect :str
