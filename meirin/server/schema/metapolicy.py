from typing import Optional

from pydantic import BaseModel

class MetaPolicyInput(BaseModel):
    name   :str
    match  :str
    mode   :str

class MetaPolicySchema(BaseModel):
    """元策略
    """
    id :Optional[int]

    name   :str
    match  :str
    mode   :str
